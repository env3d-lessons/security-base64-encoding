import os
import pathlib
import pytest
import re

@pytest.fixture
def qrcode_sh_content():
    with open('qrcode.sh') as f:
        return f.read()        

def test_qr_code_executable():
    permissions = os.popen('stat -c %A qrcode.sh').read().strip()
    assert permissions.endswith('x'), "Must be executable with permission 755"

def test_qr_code_hashbang(qrcode_sh_content):
    assert '#!/bin/bash' in qrcode_sh_content, "Missing hashbang line"
        
def test_qr_code_content_type(qrcode_sh_content):
    assert re.search(r'content-type.*text/html', qrcode_sh_content, re.IGNORECASE), (
        "Must have the correct content-type" )

def test_qrencode_usage(qrcode_sh_content):
    assert re.search(r'qrencode', qrcode_sh_content), (
        "Must use qrencode command" )

def test_base64_usage(qrcode_sh_content):
    assert re.search(r'base64', qrcode_sh_content), (
        "Must use qrencode command" )

def test_qr_no_arguments():
    content = os.popen(
        f'./qrcode.sh'
    ).read()
    assert 'img' not in content, "Do not output image if no parameter provided"

@pytest.fixture
def qrcontent():
    content = os.popen(
        f'QUERY_STRING=bye ./qrcode.sh bye'
    ).read()
    return content
    
def test_qr_code_execute1(qrcontent):    
    assert 'data:image/png;base64' in qrcontent

def test_qr_code_execute2(qrcontent):
    assert 'iVBORw0KGgoAAAANSUhEUgAAAFcAAABXAQMAAABLBksvAAAABlBMVEUAAAD' in qrcontent

def test_qr_code_execute3(qrcontent):
    assert 'Tffp2Y1nYMbF6weprULZQpneOvv8TS97' in qrcontent

def test_qr_code_execute4():
    content1 = os.popen(
        f'QUERY_STRING=abc ./qrcode.sh abc'
    ).read()
    content2 = os.popen(
        f'QUERY_STRING=123 ./qrcdoe.sh 123'
    ).read()
    assert content1 != content2, "Script seems to be producing the same output for the different input"

    
