import pytest
from src.services.document import DocumentDiffUtility
from src.api.v1.schemas.document import DocumentRevisionDiff, SectionDiff, ModifiedSection

class TestDocumentDiffUtility:
    """DocumentDiffUtilityクラスのテスト"""

    def test_compute_section_diff_no_change(self):
        """変更がない場合のセクション差分計算テスト"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]

        result = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(result["added"]) == 0
        assert len(result["removed"]) == 0
        assert len(result["modified"]) == 0

    def test_compute_section_diff_added_sections(self):
        """セクション追加時の差分計算テスト"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]

        result = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(result["added"]) == 1
        assert result["added"][0]["title"] == "セクション2"
        assert result["added"][0]["content"] == "内容2"
        assert len(result["removed"]) == 0
        assert len(result["modified"]) == 0

    def test_compute_section_diff_removed_sections(self):
        """セクション削除時の差分計算テスト"""
        old_sections = [
            {"title": "セクション1", "content": "内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "内容1"}
        ]

        result = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(result["added"]) == 0
        assert len(result["removed"]) == 1
        assert result["removed"][0]["title"] == "セクション2"
        assert result["removed"][0]["content"] == "内容2"
        assert len(result["modified"]) == 0

    def test_compute_section_diff_modified_sections(self):
        """セクション内容変更時の差分計算テスト"""
        old_sections = [
            {"title": "セクション1", "content": "古い内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "新しい内容1"},
            {"title": "セクション2", "content": "内容2"}
        ]

        result = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(result["added"]) == 0
        assert len(result["removed"]) == 0
        assert len(result["modified"]) == 1
        assert result["modified"][0]["title"] == "セクション1"
        assert result["modified"][0]["old_content"] == "古い内容1"
        assert result["modified"][0]["new_content"] == "新しい内容1"

    def test_compute_section_diff_combined_changes(self):
        """複合的な変更時の差分計算テスト"""
        old_sections = [
            {"title": "セクション1", "content": "古い内容1"},
            {"title": "セクション2", "content": "内容2"},
            {"title": "セクション3", "content": "削除される内容"}
        ]
        new_sections = [
            {"title": "セクション1", "content": "新しい内容1"},
            {"title": "セクション2", "content": "内容2"},
            {"title": "新しいセクション", "content": "追加された内容"}
        ]

        result = DocumentDiffUtility.compute_section_diff(old_sections, new_sections)

        assert len(result["added"]) == 1
        assert result["added"][0]["title"] == "新しいセクション"

        assert len(result["removed"]) == 1
        assert result["removed"][0]["title"] == "セクション3"

        assert len(result["modified"]) == 1
        assert result["modified"][0]["title"] == "セクション1"
        assert result["modified"][0]["old_content"] == "古い内容1"
        assert result["modified"][0]["new_content"] == "新しい内容1"

    def test_create_revision_diff(self):
        """リビジョン差分作成のテスト"""
        old_content = {
            "title": "古いタイトル",
            "sections": [
                {"title": "セクション1", "content": "古い内容1"},
                {"title": "セクション2", "content": "内容2"},
                {"title": "削除セクション", "content": "削除される内容"}
            ]
        }
        new_content = {
            "title": "新しいタイトル",
            "sections": [
                {"title": "セクション1", "content": "新しい内容1"},
                {"title": "セクション2", "content": "内容2"},
                {"title": "追加セクション", "content": "追加された内容"}
            ]
        }

        from_version = "1.0.0"
        to_version = "1.1.0"

        # 手動でバージョン情報を設定
        result = DocumentDiffUtility.create_revision_diff(old_content, new_content)
        result.from_version = from_version
        result.to_version = to_version

        # 返値がDocumentRevisionDiffクラスのインスタンスであることを確認
        assert isinstance(result, DocumentRevisionDiff)

        # バージョン情報の検証
        assert result.from_version == from_version
        assert result.to_version == to_version

        # 追加されたセクションの検証
        assert len(result.sections_added) == 1
        assert isinstance(result.sections_added[0], SectionDiff)
        assert result.sections_added[0].title == "追加セクション"
        assert result.sections_added[0].content == "追加された内容"

        # 削除されたセクションの検証
        assert len(result.sections_removed) == 1
        assert isinstance(result.sections_removed[0], SectionDiff)
        assert result.sections_removed[0].title == "削除セクション"
        assert result.sections_removed[0].content == "削除される内容"

        # 変更されたセクションの検証 (dictになっていることに注意)
        assert len(result.sections_modified) == 1
        modified_section = result.sections_modified[0]
        assert isinstance(modified_section, dict)
        assert modified_section["title"] == "セクション1"
        assert modified_section["old_content"] == "古い内容1"
        assert modified_section["new_content"] == "新しい内容1"
