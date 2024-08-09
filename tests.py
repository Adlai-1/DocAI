import unittest
from unittest.mock import patch
from rag_model.model import call_rag, store_chat
from rag_model.vectorize import embed_and_save


class TestDocumentAssistant(unittest.TestCase):

    @patch("rag_model.model.main_chain")
    @patch("rag_model.model.store_chat")
    def test_call_rag_basic(self, mock_store_chat, mock_main_chain):
        mock_main_chain.invoke.return_value = {"answer": "Test answer"}
        chat_memory = []
        input_text = "Test question"

        result = call_rag(input_text, chat_memory)

        self.assertEqual(result, "Test answer")
        mock_main_chain.invoke.assert_called_once_with(
            {"input": input_text, "history": chat_memory}
        )
        mock_store_chat.assert_called_once_with(chat_memory, input_text, "Test answer")

    @patch("rag_model.model.main_chain")
    @patch("rag_model.model.store_chat")
    def test_call_rag_with_existing_chat_memory(self, mock_store_chat, mock_main_chain):
        mock_main_chain.invoke.return_value = {"answer": "Follow-up answer"}
        chat_memory = [
            {"role": "human", "content": "Previous question"},
            {"role": "ai", "content": "Previous answer"},
        ]
        input_text = "Follow-up question"

        result = call_rag(input_text, chat_memory)

        self.assertEqual(result, "Follow-up answer")
        mock_main_chain.invoke.assert_called_once_with(
            {"input": input_text, "history": chat_memory}
        )
        mock_store_chat.assert_called_once_with(
            chat_memory, input_text, "Follow-up answer"
        )

    @patch("rag_model.model.main_chain")
    @patch("rag_model.model.store_chat")
    def test_call_rag_empty_response(self, mock_store_chat, mock_main_chain):
        mock_main_chain.invoke.return_value = {"answer": ""}
        chat_memory = []
        input_text = "Question with empty response"

        result = call_rag(input_text, chat_memory)

        self.assertEqual(result, "")
        mock_main_chain.invoke.assert_called_once_with(
            {"input": input_text, "history": chat_memory}
        )
        mock_store_chat.assert_called_once_with(chat_memory, input_text, "")

    @patch("rag_model.vectorize.PyMuPDFLoader")
    @patch("rag_model.vectorize.RecursiveCharacterTextSplitter")
    @patch("rag_model.vectorize.HuggingFaceEmbeddings")
    @patch("rag_model.vectorize.Chroma")
    @patch("rag_model.vectorize.config")
    def test_embed_and_save_success(
        self, mock_config, mock_chroma, mock_embeddings, mock_splitter, mock_loader
    ):
        mock_loader.return_value.load.return_value = ["doc1", "doc2"]
        mock_splitter.return_value.split_documents.return_value = ["split1", "split2"]
        mock_config.__getitem__.return_value = {"embedding": "test_model"}

        result = embed_and_save("test.pdf")

        self.assertEqual(result, "Added new document successfully!")
        mock_loader.assert_called_once_with("./docs/test.pdf")
        mock_splitter.assert_called_once_with(chunk_size=1000)
        mock_embeddings.assert_called_once_with(model_name="test_model")
        mock_chroma.from_documents.assert_called_once()

    @patch("rag_model.vectorize.PyMuPDFLoader")
    def test_embed_and_save_file_not_found(self, mock_loader):
        mock_loader.side_effect = ValueError("File not found")

        result = embed_and_save("nonexistent.pdf")

        self.assertEqual(result, "Can't find nonexistent.pdf in docs directory!")

    @patch("rag_model.vectorize.PyMuPDFLoader")
    def test_embed_and_save_general_error(self, mock_loader):
        mock_loader.side_effect = Exception("General error")

        result = embed_and_save("error.pdf")

        self.assertEqual(result, "Error occured whiles performing embedding.")

    @patch("rag_model.vectorize.PyMuPDFLoader")
    @patch("rag_model.vectorize.RecursiveCharacterTextSplitter")
    @patch("rag_model.vectorize.HuggingFaceEmbeddings")
    @patch("rag_model.vectorize.Chroma")
    @patch("rag_model.vectorize.config")
    def test_embed_and_save_embedding_error(
        self, mock_config, mock_chroma, mock_embeddings, mock_splitter, mock_loader
    ):
        mock_loader.return_value.load.return_value = ["doc1", "doc2"]
        mock_splitter.return_value.split_documents.return_value = ["split1", "split2"]
        mock_config.__getitem__.return_value = {"embedding": "test_model"}
        mock_chroma.from_documents.side_effect = Exception("Embedding error")

        result = embed_and_save("test.pdf")

        self.assertEqual(result, "Error occured whiles performing embedding.")

    def test_store_chat(self):
        memory = []
        store_chat(memory, "How are you?", "I'm good, thank you!")
        self.assertEqual(len(memory), 2)
        self.assertEqual(memory[0].content, "How are you?")
        self.assertEqual(memory[1].content, "I'm good, thank you!")


if __name__ == "__main__":
    unittest.main()
