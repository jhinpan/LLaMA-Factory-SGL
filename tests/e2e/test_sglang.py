# Copyright 2025 the LlamaFactory team.
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

import os
import sys

import pytest


# Check if SGLang is installed
try:
    import importlib.util

    SGLANG_AVAILABLE = importlib.util.find_spec("sglang") is not None
except ImportError:
    SGLANG_AVAILABLE = False

# Import directly from src
from llamafactory.chat import ChatModel


# Configuration for tests
TINY_LLAMA = os.getenv("TINY_LLAMA", "llamafactory/tiny-random-Llama-3")

# Basic inference args
INFER_ARGS = {
    "model_name_or_path": TINY_LLAMA,
    "finetuning_type": "lora",
    "template": "llama3",
    "infer_dtype": "float16",
    "infer_backend": "sglang",  # Use the SGLang backend
    "do_sample": False,
    "max_new_tokens": 1,
}

# Test messages
MESSAGES = [
    {"role": "user", "content": "Hi"},
]

# Expected response from the test model
EXPECTED_RESPONSE = "_rho"


@pytest.mark.skipif(
    not SGLANG_AVAILABLE,
    reason="SGLang is not installed",
)
def test_chat():
    """Test the SGLang engine's basic chat functionality"""
    chat_model = ChatModel(INFER_ARGS)
    assert chat_model.engine_type == "sglang", f"Expected engine type 'sglang', got '{chat_model.engine_type}'"
    response = chat_model.chat(MESSAGES)[0]
    assert (
        response.response_text == EXPECTED_RESPONSE
    ), f"Expected '{EXPECTED_RESPONSE}', got '{response.response_text}'"


@pytest.mark.skipif(
    not SGLANG_AVAILABLE,
    reason="SGLang is not installed",
)
def test_stream_chat():
    """Test the SGLang engine's streaming chat functionality"""
    chat_model = ChatModel(INFER_ARGS)
    response = ""
    for token in chat_model.stream_chat(MESSAGES):
        response += token

    assert response == EXPECTED_RESPONSE, f"Expected '{EXPECTED_RESPONSE}', got '{response}'"


# Run tests if executed directly
if __name__ == "__main__":
    if not SGLANG_AVAILABLE:
        print("SGLang is not available. Please install it with 'pip install sglang'")
        sys.exit(1)

    print("Testing SGLang engine...")
    test_chat()
    test_stream_chat()
    print("All SGLang tests passed!")
