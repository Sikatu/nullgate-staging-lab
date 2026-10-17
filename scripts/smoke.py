#!/usr/bin/env python3
"""Run a disposable loopback-only Purpur server and record truthful boot evidence.

This does NOT simulate legitimate Mojang/Microsoft account authentication or real player load.
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BAD = re.compile(r'NoSuchMethodError|NoClassDefFoundError|IncompatibleClassChangeError|AbstractMethodError|VerifyError|ExceptionInInitializerError|Could not pass event .* to Nullgate|Error occurred while enabling Nullgate|Could not load .*Nullgate', re.I)
READY = re.compile(r'Done \([0-9.,]+s\)!|Done \([0-9.,]+s\)', re.I)
ENABLE = re.compile(r'\[Nullgate\].*(?:Enabling Nullgate|enabled|Loading Nullgate)', re.I)

def dependency_inventory(directory):
    names = [f.name.lower() for f in directory.glob('*.jar')]
    return {'PacketEvents':any('packetevents' in f for f in names),
            'Floodgate':any('floodgate' in f for f in names),
            'Geyser-Spigot':any('geyser' in f for f in names)}

def evaluate(lines, exitcode, deps, strict=False):
    joined='\n'.join(lines)
    errors = [line.strip() for line in lines if BAD.search(line)]
    ready = bool(READY.search(joined))
    enabled = bool(ENABLE.search(joined))
    missing = [k for k,v in deps.items() if not v]
    clean_shutdown = exitcode == 0
    passing = ready and enabled and clean_shutdown and not errors and (not strict or not missing)
    return {'verdict':'PASS' if passing else 'FAIL','server_ready':ready,
            'nullgate_startup_marker':enabled,'clean_shutdown':clean_shutdown,
            'linkage_or_plugin_event_errors':errors[:25],
            'dependencies_present':deps,'missing_integration_dependencies':missing,
            'strict_dependency_gate':strict,'test_scope':'PURPUR_LOOPBACK_BOOT_ONLY',
            'real_java_premium_proof_tested':False,'real_bedrock_login_tested':False,
            'real_multiplayer_stress_tested':False,'production_certified':False}

def run(server, runtime, max_wait, soak, strict):
    runtime.mkdir(parents=True,exist_ok=True)
    plugins=runtime/'plugins'; plugins.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'test-assets/Nullgate.jar',plugins/'Nullgate.jar')
    depsdir=ROOT/'test-assets/dependencies'
    for dep in depsdir.glob('*.jar'):
        shutil.copy2(dep,plugins/dep.name)
    deps=dependency_inventory(plugins)
    (runtime/'eula.txt').write_text('eula=true\n')
    (runtime/'server.properties').write_text('''# Disposable CI staging server, never production
server-ip=127.0.0.1
server-port=25565
online-mode=false
enforce-secure-profile=false
spawn-protection=0
max-players=20
motd=Nullgate CI Staging Only
view-distance=2
simulation-distance=2
generate-structures=false
sync-chunk-writes=true
enable-rcon=false
enable-query=false
''')
    shutil.copy2(server,runtime/'purpur.jar')
    logpath=runtime/'ci-console.log'
    lines=[]
    with logpath.open('w',encoding='utf-8',errors='replace') as log:
        process=subprocess.Popen(['java','-Xms256M','-Xmx3G','-jar','purpur.jar','--nogui'],cwd=runtime,
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            text=True,bufsize=1,errors='replace')
        def reader():
            for line in process.stdout:
                lines.append(line.rstrip('\n'))
                log.write(line)
                log.flush()
        t=threading.Thread(target=reader,daemon=True);t.start()
        started=time.monotonic(); ready_at=None
        while time.monotonic()-started<max_wait:
            if any(READY.search(x) for x in lines):
                ready_at=time.monotonic();break
            if process.poll() is not None:break
            time.sleep(.3)
        if ready_at:
            deadline=ready_at+soak
            while time.monotonic()<deadline and process.poll() is None:
                time.sleep(.3)
        if process.poll() is None:
            try:
                process.stdin.write('stop\n');process.stdin.flush()
            except (BrokenPipeError,OSError):pass
            try:process.wait(timeout=40)
            except subprocess.TimeoutExpired:
                process.kill();process.wait(timeout=10)
        t.join(timeout=10)
    result=evaluate(lines,process.returncode,deps,strict)
    result['elapsed_seconds']=round(time.monotonic()-started,2)
    result['server_jar']=server.name
    output=ROOT/'smoke-report.json';output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('Log last 35 lines:\n'+'\n'.join(lines[-35:]))
    return 0 if result['verdict']=='PASS' else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--server',type=pathlib.Path,required=True)
    ap.add_argument('--runtime',type=pathlib.Path,default=ROOT/'runtime')
    ap.add_argument('--max-wait',type=int,default=240)
    ap.add_argument('--soak',type=int,default=60)
    ap.add_argument('--strict-dependencies',action='store_true')
    args=ap.parse_args()
    if not args.server.is_file():ap.error(f'server jar missing: {args.server}')
    sys.exit(run(args.server.resolve(),args.runtime.resolve(),args.max_wait,args.soak,args.strict_dependencies))
