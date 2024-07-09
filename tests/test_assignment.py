import os
import pathlib
import pytest
import re

@pytest.fixture
def my_server_name():
    os.popen('cp /usr/lib/cgi-bin/security-base64-encoding/qrcode.sh .').read()
    server_name = os.popen("sudo apachectl -S | grep -o -P '\\S+wmdd4950.com'").read()
    if not pathlib.Path('server_name.txt').is_file():
        f = open('server_name.txt','w')
        f.write(server_name)
        f.close()

    return open('server_name.txt').read().strip()

def test_qr_code_hashbang(my_server_name):
    with open('qrcode.sh') as f:
        content = f.read()
        assert '#!/bin/bash' in content, "Must be an executable secript"
        
def test_qr_code_content_type(my_server_name):
    with open('qrcode.sh') as f:
        content = f.read()
        assert re.search(r'content-type.*text/html', content, re.IGNORECASE), (
            "Must have the correct content-type" )

@pytest.fixture
def qrcontent(my_server_name):
    content = os.popen(
        f'curl -s https://{my_server_name}/cgi-bin/security-base64-encoding/qrcode.sh?bye'
    ).read()
    return content
    
def test_qr_code_execute(my_server_name, qrcontent):    
    assert 'data:image/png;base64' in qrcontent

def test_qr_code_execute(my_server_name, qrcontent):
    assert 'iVBORw0KGgoAAAANSUhEUgAAAFcAAABXAQMAAABLBksvAAAABlBMVEUAAAD' in qrcontent
    
