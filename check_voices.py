import asyncio
import edge_tts

async def list_voices():
    voices = await edge_tts.list_voices()
    indian_voices = [v for v in voices if any(lang in v['LocaleName'] for lang in ["Tamil", "Hindi", "Telugu", "Malayalam", "Bengali"])]
    
    print(f"Found {len(indian_voices)} Indian voices:")
    for v in indian_voices:
        print(f"- {v['ShortName']} ({v['Gender']})")

if __name__ == "__main__":
    asyncio.run(list_voices())
