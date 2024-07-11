import os
import pathlib
import pytest
import re

@pytest.fixture
def my_server_name():
    return 'localhost'

@pytest.fixture
def qrcode_sh_content():
    with open('qrcode.sh') as f:
        return f.read()        

def test_qr_code_executable():
    permissions = os.popen('stat -c %A qrcode.sh').read().strip()
    assert permissions.endswith('x'), "Must be executable with permission 755"

def test_qr_code_hashbang(my_server_name, qrcode_sh_content):
    assert '#!/bin/bash' in qrcode_sh_content, "Missing hashbang line"
        
def test_qr_code_content_type(my_server_name, qrcode_sh_content):
    assert re.search(r'content-type.*text/html', qrcode_sh_content, re.IGNORECASE), (
        "Must have the correct content-type" )

def test_qrencode_usage(my_server_name, qrcode_sh_content):
    assert re.search(r'qrencode', qrcode_sh_content), (
        "Must use qrencode command" )

def test_base64_usage(my_server_name, qrcode_sh_content):
    assert re.search(r'base64', qrcode_sh_content), (
        "Must use qrencode command" )

@pytest.fixture
def qrcontent(my_server_name):
    content = os.popen(
        f'curl -s {my_server_name}/cgi-bin/qrcode.sh?bye'
    ).read()
    return content
    
def test_qr_code_execute1(my_server_name, qrcontent):    
    assert 'data:image/png;base64' in qrcontent

def test_qr_code_execute2(my_server_name, qrcontent):
    assert 'iVBORw0KGgoAAAANSUhEUgAAAFcAAABXAQMAAABLBksvAAAABlBMVEUAAAD' in qrcontent

def test_qr_code_execute3(my_server_name, qrcontent):
    assert 'Tffp2Y1nYMbF6weprULZQpneOvv8TS97' in qrcontent

def test_qr_code_execute4(my_server_name):
    content1 = os.popen(
        f'curl -s {my_server_name}/cgi-bin/qrcode.sh?abc'
    ).read()
    content2 = os.popen(
        f'curl -s {my_server_name}/cgi-bin/qrcode.sh?123'
    ).read()
    assert content1 != content2, "Script seems to be producing the same output for the different input"

    
