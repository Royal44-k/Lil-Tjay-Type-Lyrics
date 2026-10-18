"""Compile editorial and Suno handoff books from preserved local snapshots."""
from pathlib import Path
import csv,json,re,hashlib,zipfile
from prompt_extensions import EXTRAS

ROOT=Path(__file__).resolve().parent
TRACKS=json.loads((ROOT/'TRACKS.json').read_text(encoding='utf-8'))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def csvwrite(path,fields,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def section(label,value):return f'### {label}\n\n```text\n{value.strip()}\n```\n'

index=[];checked=[]
for album,album_dir,out in [('SECOND LIFE','SECOND-LIFE','04-SECOND-LIFE-SUNO.md'),('SECOND LIFE+','SECOND-LIFE-PLUS','05-SECOND-LIFE-PLUS-SUNO.md')]:
    book=[f'# {album} — 完整 Suno 制作提示词\n',
          '每首单独生成。第一轮只复制 Title / Style / Exclude / Lyrics 四栏到相应位置。其他段落是人声、纯伴奏或已有候选的修正提示，一次选一个问题处理，不全部叠加进 Style。中文说明不进入歌词框。\n',
          '歌词和主 Style / Exclude 为既有版本原样收录。附加方向是本轮新写。所有 BPM、调性、声部和段落数都是制作目标，未假定文本可精确控制音频。操作流程见 07-SUNO-WORKFLOW.md。\n']
    for t in [t for t in TRACKS if t['album']==album]:
        p=ROOT/'suno'/album_dir/t['folder'];e=EXTRAS[t['id']]
        display=t['title']+(f" ({t['version']})" if t['kind']=='remix' else '')
        raw={name:(p/name).read_text(encoding='utf-8').strip() for name in ['LYRICS.txt','STYLE.txt','EXCLUDE.txt']}
        assert len(raw['STYLE.txt'])<=1000
        assert not re.search(r'[\u4e00-\u9fff]',raw['LYRICS.txt']+raw['STYLE.txt']+raw['EXCLUDE.txt'])
        texts={'TITLE.txt':display,'VOCAL-DIRECTION.txt':e['voice'],'INSTRUMENTAL-STYLE.txt':e['instrumental'],
               'INSTRUMENTAL-EXCLUDE.txt':'lead vocals, backing vocals, choir, spoken words, sung lyrics',
               'HOOK-REPAIR.txt':e['hook'],'ARRANGEMENT-REPAIR.txt':e['arrangement']}
        for name,value in texts.items():
            assert not re.search(r'[\u4e00-\u9fff]',value)
            (p/name).write_text(value+'\n',encoding='utf-8')
        blocks=[f'## {t["id"]} — {display}\n',e['note']+'\n',
                section('Title',display),section('Style',raw['STYLE.txt']),section('Exclude',raw['EXCLUDE.txt']),section('Lyrics',raw['LYRICS.txt']),
                '### 人声方向｜用于候选修正或录音指导\n',section('Vocal direction',e['voice']),
                '### 纯伴奏备选｜使用器乐模式，歌词留空\n',section('Instrumental Style',e['instrumental']),section('Instrumental Exclude',texts['INSTRUMENTAL-EXCLUDE.txt']),
                '### Hook 不清楚时｜已有候选的局部修正\n',section('Hook repair',e['hook']),
                '### 编排偏离时｜已有候选的局部修正\n',section('Arrangement repair',e['arrangement'])]
        (p/'PROMPT-CARD.md').write_text('\n'.join(blocks).replace('## '+t['id'],'# '+t['id'],1),encoding='utf-8')
        book+=blocks
        with (p/'ARRANGEMENT.csv').open(encoding='utf-8-sig') as f:arr=list(csv.DictReader(f))
        bars=sum(int(row['bars']) for row in arr)
        index.append(dict(album=album,track_id=t['id'],title=display,bpm_target=t['bpm'],key_target=t['key'],bars=bars,
                          planned_seconds=round(bars*240/t['bpm'],3),prompt_card=str((p/'PROMPT-CARD.md').relative_to(ROOT)),
                          unique_version='SL04' if t['id']=='SLP08' else t['id'],status='PREPRODUCTION_INPUTS_NO_AUDIO_GENERATED'))
        checked.append(dict(track_id=t['id'],style_characters=len(raw['STYLE.txt']),lyrics_characters=len(raw['LYRICS.txt']),complete_lyrics_in_book=True))
    (ROOT/out).write_text('\n'.join(book),encoding='utf-8')
csvwrite(ROOT/'PROMPT-INDEX.csv',list(index[0]),index)
for name,fields in [
 ('GENERATION-LOG.csv',['album','track_id','candidate_id','model','settings','prompt_version','source_audio','suno_url','listening_notes','decision']),
 ('PUBLICATION-LOG.csv',['asset','copy_version','actual_artist_credit','actual_release_date','platform','approved_link','published_at','status'])]:
    if not (ROOT/name).exists():csvwrite(ROOT/name,fields,[])
proof=json.loads((ROOT/'SOURCE-PROVENANCE.json').read_text(encoding='utf-8'))
for entry in proof:assert sha(ROOT/entry['copy'])==entry['sha256'],entry['copy']
a=ROOT/'suno'/'SECOND-LIFE'/'04-SECOND-LIFE';b=ROOT/'suno'/'SECOND-LIFE-PLUS'/'08-second-life'
for name in ['LYRICS.txt','STYLE.txt','EXCLUDE.txt','HOOK-GUIDE.mid','HOOK-NOTES.csv','ARRANGEMENT.csv']:
    assert (a/name).read_bytes()==(b/name).read_bytes(),name
report=dict(album_slots=len(TRACKS),unique_song_versions=len(set(x['unique_version'] for x in index)),
            original_album_slots=sum(t['album']=='SECOND LIFE' for t in TRACKS),plus_album_slots=sum(t['album']=='SECOND LIFE+' for t in TRACKS),
            preserved_assets=len(proof),preserved_assets_match=True,shared_second_life_six_files_identical=True,
            original_planned_seconds=round(sum(x['planned_seconds'] for x in index if x['album']=='SECOND LIFE'),3),
            plus_planned_seconds=round(sum(x['planned_seconds'] for x in index if x['album']=='SECOND LIFE+'),3),
            inputs=checked,audio_generated=False,publicity_published=False)
(ROOT/'QC-REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='DELIVERY-MANIFEST.json']
(ROOT/'DELIVERY-MANIFEST.json').write_text(json.dumps(dict(version='editorial-suno-v1.0',files=files),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=ROOT.parent/'SECOND-LIFE-DUOLOGY-STORY-PROMO-SUNO.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+1
    for f in files:
        value=z.read(f['path'].replace('\\','/'))
        assert hashlib.sha256(value).hexdigest()==f['sha256'] and len(value)==f['bytes']
print(json.dumps(dict(album_slots=report['album_slots'],unique_song_versions=report['unique_song_versions'],preserved_assets=len(proof),
                     book_tracks=[4,8],archive_files=len(files)+1,zip_crc_and_hashes='PASS',archive=str(archive)),indent=2))
