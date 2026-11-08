import pytest
from app.services.gnani.prisma_service import prisma_service
from app.services.gnani.timbre_service import timbre_service

@pytest.mark.asyncio
async def test_prisma_transcription_service():
    dummy_wav = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    result = await prisma_service.transcribe(
        audio_bytes=dummy_wav,
        filename="test.wav",
        language_code="en-IN"
    )
    assert "transcribed_text" in result
    assert result["confidence"] > 0.8
    assert "gnani_prisma" in result["provider"]
    assert result["latency_ms"] >= 0

@pytest.mark.asyncio
async def test_timbre_synthesis_service():
    test_text = "Step inside the vault where the ink can dry."
    result = await timbre_service.synthesize(
        text=test_text,
        voice_id="Nalini",
        language="en-IN"
    )
    assert "status" in result
    assert "provider" in result

