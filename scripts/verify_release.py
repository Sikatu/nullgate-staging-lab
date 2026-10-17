#!/usr/bin/env python3
"""Fail closed if the staged plugin is replaced or metadata is inconsistent."""
import hashlib
import json
import pathlib
import re
import sys
import zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
jar = ROOT / 'test-assets/Nullgate.jar'
expected = (ROOT / 'test-assets/Nullgate.sha256').read_text().strip().split()[0]
actual = hashlib.sha256(jar.read_bytes()).hexdigest()
with zipfile.ZipFile(jar) as z:
    descriptor = z.read('plugin.yml').decode()
    manifest = z.read('META-INF/MANIFEST.MF').decode()
    classes = [p for p in z.namelist() if p.endswith('.class')]
    assert 'name: Nullgate' in descriptor
    assert "version: '0.1.0-alpha.4.21'" in descriptor
    assert 'Implementation-Version: 0.1.0-alpha.4.21' in manifest
    assert 'com/ellipsissmp/nullgate/NullgatePlugin.class' in classes
assert actual == expected, f'JAR hash mismatch: actual={actual} expected={expected}'
report = {'plugin':'Nullgate','version':'0.1.0-alpha.4.21', 'sha256':actual,
          'compiled_classes':len(classes),'integrity':'PASS',
          'production_certified': False, 'real_authentication_tested': False}
print(json.dumps(report,indent=2))
(ROOT / 'integrity-report.json').write_text(json.dumps(report,indent=2)+'\n')
