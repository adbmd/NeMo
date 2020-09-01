# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional

from transformers import (
    ALBERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    BERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    DISTILBERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    ROBERTA_PRETRAINED_MODEL_ARCHIVE_LIST,
    AlbertConfig,
    BertConfig,
    DistilBertConfig,
    RobertaConfig,
)

from nemo.collections.nlp.modules.common.huggingface.albert import AlbertEncoder
from nemo.collections.nlp.modules.common.huggingface.bert import BertEncoder
from nemo.collections.nlp.modules.common.huggingface.distilbert import DistilBertEncoder
from nemo.collections.nlp.modules.common.huggingface.roberta import RobertaEncoder
from nemo.utils import logging

__all__ = ['HUGGINGFACE_MODELS', 'get_huggingface_lm_model', 'get_huggingface_pretrained_lm_models_list']


HUGGINGFACE_MODELS = {
    'bert': {
        'default': 'bert-base-uncased',
        'class': BertEncoder,
        'config': BertConfig,
        'pretrained_model_list': BERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    },
    'distilbert': {
        'default': 'distilbert-base-uncased',
        'class': DistilBertEncoder,
        'config': DistilBertConfig,
        'pretrained_model_list': DISTILBERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    },
    'roberta': {
        'default': 'roberta-base',
        'class': RobertaEncoder,
        'config': RobertaConfig,
        'pretrained_model_list': ROBERTA_PRETRAINED_MODEL_ARCHIVE_LIST,
    },
    'albert': {
        'default': 'albert-base-v2',
        'class': AlbertEncoder,
        'config': AlbertConfig,
        'pretrained_model_list': ALBERT_PRETRAINED_MODEL_ARCHIVE_LIST,
    },
}


def get_huggingface_lm_model(model_type: str, 
    pretrained_model_name: Optional[str] = None, config_dict: Optional[dict] = None, config_file: Optional[str] = None
):
    '''
    Returns lm model instantiated with Huggingface
    Args:
        model_type: model type. Valid options are the keys in HUGGINGFACE_MODELS
        pretrained_mode_name: specify this to instantiate pretrained model from Huggingface,
            e.g. bert-base-cased. For entire list, see get_huggingface_pretrained_lm_models_list().
        config_dict: model configuration dictionary used to instantiate Huggingface model from scratch
        config_file: path to model configuration file used to instantiate Huggingface model from scratch
    '''

    # assumes that model configuration is correct, otherwise will pass on Huggingface's model instantiation error
    model_class = HUGGINGFACE_MODELS[model_type]['class']
    if config_file:
        config_class = HUGGINGFACE_MODELS[model_type]['config']
        return model_class(config_class.from_json_file(config_file))
    elif config_dict:
        config_class = HUGGINGFACE_MODELS[model_type]['config']
        return model_class(config=config_class(**config_dict))
    else:
        return model_class.from_pretrained(pretrained_model_name)


def get_huggingface_pretrained_lm_models_list() -> List[str]:
    '''
    Returns the list of supported HuggingFace HUGGINGFACE_MODELS
    '''
    huggingface_models = []
    for model in HUGGINGFACE_MODELS:
        model_names = HUGGINGFACE_MODELS[model]['pretrained_model_list']
        huggingface_models.extend(model_names)
    return huggingface_models
