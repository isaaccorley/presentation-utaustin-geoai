"""Single Manim entrypoint for the GeoAI talk scenes."""

from scenes.s01_cloud_native_stack import S01_CloudNativeStack as _S01_CloudNativeStack
from scenes.s02_inference_pipeline import S02_InferencePipeline as _S02_InferencePipeline
from scenes.s03_torchgeo_sampling import S03_TorchGeoSampling as _S03_TorchGeoSampling
from scenes.s04_embedding_retrieval import S04_EmbeddingRetrieval as _S04_EmbeddingRetrieval
from scenes.s05_cog_byte_range import S05_COGByteRange as _S05_COGByteRange
from scenes.s06_stac_search_fanout import S06_STACSearchFanout as _S06_STACSearchFanout
from scenes.s07_geo_parquet_pushdown import S07_GeoParquetPushdown as _S07_GeoParquetPushdown
from scenes.s08_contrastive_learning import S08_ContrastiveLearning as _S08_ContrastiveLearning
from scenes.s09_mae_masked_modeling import S09_MAEMaskedModeling as _S09_MAEMaskedModeling
from scenes.s10_pixel_vs_patch_embedding import (
    S10_PixelVsPatchEmbedding as _S10_PixelVsPatchEmbedding,
)
from scenes.s12_cloud_native_vs_download import (
    S12_CloudNativeVsDownload as _S12_CloudNativeVsDownload,
)
from scenes.s13_production_pipeline import S13_ProductionPipeline as _S13_ProductionPipeline
from scenes.s14_cng_timeline import S14_CNGTimeline as _S14_CNGTimeline
from scenes.s16_flywheel import S16_Flywheel as _S16_Flywheel


class S01_CloudNativeStack(_S01_CloudNativeStack):
    pass


class S02_InferencePipeline(_S02_InferencePipeline):
    pass


class S03_TorchGeoSampling(_S03_TorchGeoSampling):
    pass


class S04_EmbeddingRetrieval(_S04_EmbeddingRetrieval):
    pass


class S05_COGByteRange(_S05_COGByteRange):
    pass


class S06_STACSearchFanout(_S06_STACSearchFanout):
    pass


class S07_GeoParquetPushdown(_S07_GeoParquetPushdown):
    pass


class S08_ContrastiveLearning(_S08_ContrastiveLearning):
    pass


class S09_MAEMaskedModeling(_S09_MAEMaskedModeling):
    pass


class S10_PixelVsPatchEmbedding(_S10_PixelVsPatchEmbedding):
    pass


class S12_CloudNativeVsDownload(_S12_CloudNativeVsDownload):
    pass


class S13_ProductionPipeline(_S13_ProductionPipeline):
    pass


class S14_CNGTimeline(_S14_CNGTimeline):
    pass


class S16_Flywheel(_S16_Flywheel):
    pass


__all__ = [
    "S01_CloudNativeStack",
    "S02_InferencePipeline",
    "S03_TorchGeoSampling",
    "S04_EmbeddingRetrieval",
    "S05_COGByteRange",
    "S06_STACSearchFanout",
    "S07_GeoParquetPushdown",
    "S08_ContrastiveLearning",
    "S09_MAEMaskedModeling",
    "S10_PixelVsPatchEmbedding",
    "S12_CloudNativeVsDownload",
    "S13_ProductionPipeline",
    "S14_CNGTimeline",
    "S16_Flywheel",
]
