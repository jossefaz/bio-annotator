import os

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError
from bio_annotator.common.exceptions import FileMissingError
from bio_annotator.schemas.variant import Variant


class Nirvana(AsyncAnnotator):

    def __init__(self, annotator_name):
        super().__init__(annotator_name)
        self.output_file = ''
        self.input_file = ''

    @classmethod
    @property
    def executable(cls):
        return os.getenv('NIRVANA_EXC')

    @classmethod
    @property
    def bin(cls):
        return os.getenv('NIRVANA_BIN')

    @classmethod
    @property
    def data_path(self):
        return os.getenv('NIRVANA_DATA')

    @classmethod
    def sanity_check(cls):
        if not all([cls.executable, cls.data_path, cls.bin]):
            raise AnnotatorConfigurationMissingError(cls.__name__)

    @property
    def nirvana_cache(self):
        return f"{self.data_path}/Cache/{self.human_reference}/Both"

    @property
    def nirvana_reference(self):
        return f"{self.data_path}/References/Homo_sapiens.{self.human_reference}.Nirvana.dat"

    @property
    def nirvana_supplementary(self):
        return f"{self.data_path}/SupplementaryAnnotation/{self.human_reference}"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def execute(self, *args, **kwargs):
        file_name, file_ext = os.path.splitext(self.input_file)
        self.output_file = f"{os.getcwd()}/{file_name}.json.gz"
        cmd_args = ["-c", self.nirvana_cache,
                    "-r", self.nirvana_reference,
                    "--sd", self.nirvana_supplementary,
                    "--in", self.input_file,
                    "-o", f"{os.getcwd()}/{file_name}", *args]
        return await super().annotate_batch(*cmd_args, **kwargs)

    async def annotate_one(self, variant: Variant, *args, **kwargs):
        self.input_file = await variant.to_vcf()
        self.human_reference = str(variant.human_reference.value)
        return await self.execute(*args, **kwargs)

    async def annotate_batch(self, *args, **kwargs):
        self.ensure_file_exists()
        return await self.execute(*args, **kwargs)



