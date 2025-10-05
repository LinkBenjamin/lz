import builtins
import subprocess
import io
import os

import pytest

from src.main import optimize_for_seo


class DummyCompletedProcess:
	def __init__(self, returncode=0, stdout="", stderr=""):
		self.returncode = returncode
		self.stdout = stdout
		self.stderr = stderr


def test_optimize_writes_output_on_success(tmp_path, monkeypatch, capsys):
	# Arrange: create input file
	input_file = tmp_path / "draft.txt"
	input_file.write_text("This is a test draft.")

	output_file = tmp_path / "out.txt"

	# Mock subprocess.run to return successful output
	def fake_run(cmd, capture_output, text):
		assert 'ollama' in cmd[0] or cmd[0].endswith('ollama')
		return DummyCompletedProcess(returncode=0, stdout="- Improved keyword usage\n- Minor wording tweaks")

	monkeypatch.setattr(subprocess, 'run', fake_run)

	# Act
	optimize_for_seo(str(input_file), str(output_file))

	# Assert: output file created with mocked content
	assert output_file.exists()
	content = output_file.read_text(encoding='utf-8')
	assert "Improved keyword usage" in content


def test_optimize_handles_subprocess_error(tmp_path, monkeypatch, capsys):
	# Arrange
	input_file = tmp_path / "draft.txt"
	input_file.write_text("Some draft content")
	output_file = tmp_path / "out.txt"

	# Mock subprocess.run to simulate error
	def fake_run(cmd, capture_output, text):
		return DummyCompletedProcess(returncode=1, stdout="", stderr="something went wrong")

	monkeypatch.setattr(subprocess, 'run', fake_run)

	# Act
	optimize_for_seo(str(input_file), str(output_file))

	# Capture printed error
	captured = capsys.readouterr()
	assert "Error:" in captured.out
	# Ensure no output file was written
	assert not output_file.exists()
