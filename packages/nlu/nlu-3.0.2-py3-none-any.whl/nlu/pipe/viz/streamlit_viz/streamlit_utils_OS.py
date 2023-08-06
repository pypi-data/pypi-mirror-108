from sparknlp.annotator import NerConverter,DependencyParserModel
from typing import List, Tuple, Optional, Dict
import streamlit as st
from nlu.utils.modelhub.modelhub_utils import ModelHubUtils
import numpy as np
import pandas as pd
from sparknlp.annotator import *
import nlu
class StreamlitUtilsOS():
    classifers_OS = [ ClassifierDLModel, LanguageDetectorDL, MultiClassifierDLModel, NerDLModel, NerCrfModel, YakeModel, PerceptronModel, SentimentDLModel,
                      SentimentDetectorModel, ViveknSentimentModel, DependencyParserModel, TypedDependencyParserModel, T5Transformer, MarianTransformer, NerConverter]
    @staticmethod
    def get_classifier_cols(pipe):
        classifier_cols = []
        for c in pipe.components:
            if type(c.model) in StreamlitUtilsOS.classifers_OS :
                classifier_cols += pipe.anno2final_cols[c.model]
        return  classifier_cols

    @staticmethod
    def get_embed_cols(pipe):
        classifier_cols = []
        embedders = StreamlitUtilsOS.find_all_embed_components(pipe)
        for c in embedders: classifier_cols += pipe.anno2final_cols[c.model]
        return  classifier_cols

    @staticmethod
    def find_embed_col(df, search_multi=False):
        """Find col that contains embed"""
        if not search_multi:
            for c in df.columns:
                if 'embed'in c : return c
        else:
            e_cols =[]
            for c in df.columns:
                if 'embed'in c : e_cols.append(c)
        return  e_cols


    @staticmethod
    def find_embed_component(p):
        """Find first embed  component in pipe"""
        for c in p.components :
            if 'embed' in c.info.outputs[0] : return c
        st.warning("No Embed model in pipe")
        return None

    @staticmethod
    def find_all_classifier_components(pipe):
        """Find ALL classifier component in pipe"""
        classifier_comps = []
        for c in pipe.components:
            if type(c.model) in StreamlitUtilsOS.classifers_OS :classifier_comps.append(c)
        return  classifier_comps
    @staticmethod
    def find_all_embed_components(p):
        """Find ALL  embed component in pipe"""
        cs = []
        for c in p.components :
            if 'embed' in c.info.outputs[0] and 'chunk' not  in c.info.outputs[0]: cs.append(c)
        if len(cs) == 0 : st.warning("No Embed model in pipe")
        return cs

    @staticmethod
    def extract_name(component_or_pipe):
        name =''
        if hasattr(component_or_pipe,'info') :
            if hasattr(component_or_pipe.info,'nlu_ref') : name = component_or_pipe.info.nlu_ref
            elif hasattr(component_or_pipe,'storage_ref') : name = component_or_pipe.info.storage_ref
            elif hasattr(component_or_pipe,'nlp_ref') : name = component_or_pipe.info.nlp_ref
        elif hasattr(component_or_pipe,'nlu_ref') : name = component_or_pipe.nlu_ref
        return name


    @staticmethod
    def find_ner_model(p):
        """Find NER component in pipe"""
        from sparknlp.annotator import NerDLModel,NerCrfModel
        for c in p.components :
            if isinstance(c.model,(NerDLModel,NerCrfModel)):return c.model
        st.warning("No NER model in pipe")
        return None

    @staticmethod
    def get_NER_tags_in_pipe(p):
        """Get NER tags in pipe, used for showing visualizable tags"""
        n = StreamlitUtilsOS.find_ner_model(p)
        if n is None : return []
        classes_predicted_by_ner_model = n.getClasses()
        split_iob_tags = lambda s : s.split('-')[1] if '-' in s else ''
        classes_predicted_by_ner_model = list(map(split_iob_tags,classes_predicted_by_ner_model))
        while '' in classes_predicted_by_ner_model : classes_predicted_by_ner_model.remove('')
        classes_predicted_by_ner_model = list(set(classes_predicted_by_ner_model))
        return classes_predicted_by_ner_model

    @staticmethod
    @st.cache(allow_output_mutation=True)
    def get_pipe(model='ner'): return nlu.load(model)