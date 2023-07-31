import json
import os
import urllib.parse

import streamlit as st
import streamlit.components.v1 as components

absolute_path = os.path.dirname(os.path.abspath(__file__))
frontend_path = absolute_path

evaluate_js = components.declare_component(
    "streamlit_localstorage",
    path=frontend_path
)

LOCALSTORAGE_SESSION_KEY = 'LOCALSTORAGE_SESSION_KEY'


class LocalStorageManager:
    def __init__(self):
        self._items_to_save = []
        self._items_to_delete = []
        response = evaluate_js(js_expressions=f'get_all_localstorage()',
                               key=f'get_all_localstorage')

        items = {}
        if response is not None:
            for item in response:
                items[item[0]] = json.loads(item[1])
            st.session_state[LOCALSTORAGE_SESSION_KEY] = items

    @staticmethod
    def ready() -> bool:
        return LOCALSTORAGE_SESSION_KEY in st.session_state

    def set_localstorage(self, name, value):
        st.session_state[LOCALSTORAGE_SESSION_KEY][name] = value
        self._items_to_save.append((name, value))

    def get_localstorage(self, name):
        if not self.ready():
            raise LocalStorageNotReady()

        return st.session_state[LOCALSTORAGE_SESSION_KEY][name] if name in st.session_state[
            LOCALSTORAGE_SESSION_KEY] else None

    def delete_localstorage(self, name):
        if name in st.session_state[LOCALSTORAGE_SESSION_KEY]:
            del st.session_state[LOCALSTORAGE_SESSION_KEY][name]
            self._items_to_delete.append(name)

    def save(self):
        items_to_save = []
        if len(self._items_to_save) > 0:
            for item in self._items_to_save:
                items_to_save.append({'key': item[0], 'value': item[1]})

        params = {
            'items_to_save': items_to_save,
            'items_to_delete': self._items_to_delete
        }
        serialized_params = urllib.parse.quote(json.dumps(params))
        self._items_to_save.clear()
        self._items_to_delete.clear()
        return evaluate_js(js_expressions=f'sync_localstorage(\'{serialized_params}\')',
                           key=f'sync_localstorage')


class LocalStorageNotReady(Exception):
    pass
