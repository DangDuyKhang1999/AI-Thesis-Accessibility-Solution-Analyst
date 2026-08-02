# PowerShell helper: install gTTS and run Vietnamese TTS generation
pip install gTTS
python .\scripts\legacy\generate_gtts_vi.py --in output\description_vi.txt --out output\description_vi_gtts.mp3
if ($LASTEXITCODE -eq 0) { Write-Host "gTTS generation completed." } else { Write-Host "gTTS generation failed with code $LASTEXITCODE" }
