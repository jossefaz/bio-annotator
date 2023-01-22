from dataclasses import dataclass

@dataclass
class RoutesRegistry:
    SINGLE_ANNOTATION = f"/annotation/{'{annotator_name}'}"
    BATCH_ANNOTATION = f"/annotation/{'{annotator_name}/batch/{assembly}'}"
