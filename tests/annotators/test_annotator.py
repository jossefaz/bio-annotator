import pytest

from bio_annotator.annotators.annotator import AsyncAnnotator


class TestAsyncAnnotator:

    @pytest.mark.asyncio
    @pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
    async def test_create_annotator_valid_name(self, annotator, variant_schema_factory):
        annotator_impl = AsyncAnnotator.create_annotator(annotator.__name__)
        assert isinstance(annotator_impl, annotator)

    @pytest.mark.asyncio
    async def test_create_annotator_invalid_name(self):
        with pytest.raises(ValueError, match="Invalid annotator name: invalid_name"):
            AsyncAnnotator.create_annotator('invalid_name')

    @pytest.mark.asyncio
    @pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
    async def test_async_annotator_context_manager_valid_name(self, annotator, monkeypatch):
        async with AsyncAnnotator(annotator.__name__) as annotator_impl:
            assert isinstance(annotator_impl, annotator)
            monkeypatch.setattr(annotator_impl, 'executable_bin', 'echo')
            await annotator_impl.annotate_batch(f"{annotator_impl} works as expected")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("annotator", AsyncAnnotator.__subclasses__())
    async def test_async_annotator_annotate_execute_async_cli(self, annotator, monkeypatch):
        async with AsyncAnnotator(annotator.__name__) as annotator_impl:
            assert isinstance(annotator_impl, annotator)
            monkeypatch.setattr(annotator_impl, 'executable_bin', "echo")
            stdout, stderr = await annotator_impl.annotate_batch(f"{annotator_impl} works as expected")
            assert f"{annotator_impl} works as expected" in str(stdout)

    @pytest.mark.asyncio
    async def test_async_annotator_context_manager_invalid_name(self):
        with pytest.raises(ValueError, match="Invalid annotator name: invalid_name"):
            async with AsyncAnnotator('invalid_name') as annotator:
                pass