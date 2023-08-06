#!/usr/bin/env python3

import json
from .model_data import ModelData 

def write_json(model_data: ModelData): 
    """Writes assessment JSON file"""
    
    data = {
        "model_name": model_data.model_name,
        "model_date": model_data.model_date,
        "model_version": model_data.model_version,

        "dataset_aroeira_images": model_data.dataset_aroeira_images,
        "dataset_capororoca_images": model_data.dataset_capororoca_images,
        "dataset_embauba_images": model_data.dataset_embauba_images,
        "dataset_jeriva_images": model_data.dataset_jeriva_images,
        "dataset_mulungu_images": model_data.dataset_mulungu_images,
        "dataset_pitangueira_images": model_data.dataset_pitangueira_images,
        "dataset_total_images": model_data.dataset_total_images,
        "dataset_labeler_name": model_data.dataset_labeler_name,
        "dataset_augmentation_type": model_data.dataset_augmentation_type,
        "dataset_augmentation_size": model_data.dataset_augmentation_size,
        "dataset_validation_percentage": model_data.dataset_validation_percentage,

        "tl_has_trained": model_data.tl_has_trained,
        "tl_model": model_data.tl_model,
        "tl_epochs": model_data.tl_epochs,
        "tl_learning_rate": model_data.tl_learning_rate,

        "ft_has_unfreezed": model_data.ft_has_unfreezed,
        "ft_has_trained": model_data.ft_has_trained,
        "ft_epochs": model_data.ft_epochs,
    }

    with open('assessment.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)