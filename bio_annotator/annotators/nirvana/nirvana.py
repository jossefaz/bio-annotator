import os

from bio_annotator.annotators.annotator import AsyncAnnotator
from bio_annotator.common.exceptions import AnnotatorConfigurationMissingError
from bio_annotator.schemas.variant import Variant


class Nirvana(AsyncAnnotator):

    def __init__(self, annotator_name):
        super().__init__(annotator_name)
        self._human_reference = 'GRCh37'

    @classmethod
    @property
    def executable_bin(cls):
        return os.getenv('NIRVANA_EXC')

    @classmethod
    @property
    def data_path(self):
        return os.getenv('NIRVANA_DATA')

    @classmethod
    def sanity_check(cls):
        if not all([cls.executable_bin, cls.data_path, os.getenv("NIRVANA_BIN")]):
            raise AnnotatorConfigurationMissingError(cls.__name__)

    @property
    def human_reference(self):
        return self._human_reference

    @human_reference.setter
    def human_reference(self, new_ref):
        self._human_reference = new_ref

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

    async def annotate_one(self, variant: Variant, *args, **kwargs):
        self.input_file = await variant.to_vcf()
        file_name, file_ext = os.path.splitext(self.input_file)
        self.output_file = f"{os.getcwd()}/{file_name}.json.gz"
        self.human_reference = str(variant.human_reference.value)
        cmd_args = [os.getenv("NIRVANA_BIN"),
                    "-c", self.nirvana_cache,
                    "-r", self.nirvana_reference,
                    "--sd", self.nirvana_supplementary,
                    "--in", self.input_file,
                    "-o", f"{os.getcwd()}/{file_name}"]
        return await super().annotate_batch(*cmd_args, **kwargs)


