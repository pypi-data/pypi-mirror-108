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
                ft_epochs: int
                ):
        self.model_name = str(model_name)
        self.model_date = str(model_date)
        self.model_version = str(model_version)

        self.dataset_aroeira_images = int(dataset_aroeira_images)
        self.dataset_capororoca_images = int(dataset_capororoca_images)
        self.dataset_embauba_images = int(dataset_embauba_images)
        self.dataset_jeriva_images = int(dataset_jeriva_images)
        self.dataset_mulungu_images = int(dataset_mulungu_images)
        self.dataset_pitangueira_images = int(dataset_pitangueira_images)
        self.dataset_total_images = int(dataset_total_images)
        self.dataset_labeler_name = str(dataset_labeler_name)
        self.dataset_augmentation_type = str(dataset_augmentation_type)
        self.dataset_augmentation_size = str(dataset_augmentation_size)
        self.dataset_validation_percentage = float(dataset_validation_percentage)

        self.tl_has_trained = bool(tl_has_trained)
        self.tl_model = str(tl_model)
        self.tl_epochs = int(tl_epochs)
        self.tl_learning_rate = float(tl_learning_rate)
        self.ft_has_unfreezed = bool(ft_has_unfreezed)
        self.ft_has_trained = bool(ft_has_trained)
        self.ft_epochs = int(ft_epochs)