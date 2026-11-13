"""Validate employees against the separately published skill registry."""
import argparse,hashlib,json,pathlib,re,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--skills-catalog',required=True);ap.add_argument('--check',action='store_true');args=ap.parse_args()
 skills=json.loads(pathlib.Path(args.skills_catalog).read_text());data=json.loads((ROOT/'catalog/v1/employees.json').read_text())
 if skills.get('format_version')!=1 or not skills.get('success') or data.get('format_version')!=1 or not data.get('success'):raise ValueError('Invalid catalog')
 ids={r['skill_uuid'] for r in skills['data']['items']};seen=set()
 forbidden=re.compile(rb'(?<![A-Za-z0-9_])(?:sk-[A-Za-z0-9_-]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[A-Z0-9]{16})')
 for item in data['data']['items']:
  if item['uuid'] in seen:raise ValueError('Duplicate employee')
  seen.add(item['uuid'])
  if not set(item['skill_uuids'])<=ids:raise ValueError('Missing published skill dependency: '+item['name'])
  if forbidden.search(json.dumps(item).encode()):raise ValueError('Credential-like content')
  image=item.get('avatar_url','')
  if image:
   path=pathlib.PurePosixPath(image)
   if path.is_absolute() or '..' in path.parts or not image.startswith('assets/agents/'):raise ValueError('Unsafe image')
   if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=path.stem:raise ValueError('Image digest mismatch')
 data['data']['total']=len(seen)
 stage=ROOT/'_site.next';shutil.rmtree(stage,ignore_errors=True);stage.mkdir();shutil.copytree(ROOT/'assets',stage/'assets');(stage/'catalog/v1').mkdir(parents=True)
 (stage/'catalog/v1/employees.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (stage/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>知办AI 数字员工</title><h1>知办AI 官方数字员工</h1>');(stage/'.nojekyll').touch()
 if args.check:shutil.rmtree(stage)
 else:shutil.rmtree(ROOT/'_site',ignore_errors=True);stage.rename(ROOT/'_site')
 print('Validated',len(seen),'employees and cross-repository skill references')
if __name__=='__main__':main()
