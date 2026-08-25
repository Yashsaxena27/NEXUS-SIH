import pytest
from httpx import AsyncClient
import json

@pytest.mark.asyncio
async def test_upload_valid_config(async_client: AsyncClient):
    config_content = """!
version 17.3
hostname RTR-01
banner login ^C Authorized Access Only ^C
"""
    files = {'file': ('config.txt', config_content, 'text/plain')}
    response = await async_client.post("/api/v1/scans/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "scan_id" in data
    assert data["vendor"] == "cisco"
    assert data["hostname"] == "RTR-01"

@pytest.mark.asyncio
async def test_upload_empty_file(async_client: AsyncClient):
    files = {'file': ('empty.txt', '', 'text/plain')}
    response = await async_client.post("/api/v1/scans/upload", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower() or "no readable text" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_upload_no_file(async_client: AsyncClient):
    response = await async_client.post("/api/v1/scans/upload")
    assert response.status_code == 422 # FastAPI validation error for missing File

@pytest.mark.asyncio
async def test_upload_large_file(async_client: AsyncClient):
    # Create a 6MB file in memory
    large_content = "a" * (6 * 1024 * 1024)
    files = {'file': ('large.txt', large_content, 'text/plain')}
    response = await async_client.post("/api/v1/scans/upload", files=files)
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()
