#!/usr/bin/env python3

class ModelData:
    """Model data"""
    
    # TODO validate params type
    def __init__(self, 
                model_name: str,
                model_date: str,
                model_version: str,

                dataset_aroeira_images: int,
                dataset_capororoca_images: int,
                dataset_embauba_images: int,
                dataset_jeriva_images: int,
                dataset_mulungu_images: int, 
                dataset_pitangueira_images: int,
                dataset_total_images: int,
                dataset_labeler_name: str,
                dataset_augmentation_type: str,
                dataset_augmentation_size: int,
                dataset_validation_percentage: float,

                tl_has_trained: bool,
                tl_model: str,
                tl_epochs: int,
                tl_learning_rate: float,
                
                ft_has_unfreezed: bool,
                ft_has_trained: bool,
                ft_epochs: bool
                ):
        self.model_name = model_name
        self.model_date = model_date
        self.model_version = model_version

        self.dataset_aroeira_images = dataset_aroeira_images
        self.dataset_capororoca_images = dataset_capororoca_images
        self.dataset_embauba_images = dataset_embauba_images
        self.dataset_jeriva_images = dataset_jeriva_images
        self.dataset_mulungu_images = dataset_mulungu_images
        self.dataset_pitangueira_images = dataset_pitangueira_images
        self.dataset_total_images = dataset_total_images
        self.dataset_labeler_name = dataset_labeler_name
        self.dataset_augmentation_type = dataset_augmentation_type
        self.dataset_augmentation_size = dataset_augmentation_size
        self.dataset_validation_percentage = dataset_validation_percentage

        self.tl_has_trained = tl_has_trained
        self.tl_model = tl_model
        self.tl_epochs = tl_epochs
        self.tl_learning_rate = tl_learning_rate
        self.ft_has_unfreezed = ft_has_unfreezed
        self.ft_has_trained = ft_has_trained
        self.ft_epochs = ft_epochs