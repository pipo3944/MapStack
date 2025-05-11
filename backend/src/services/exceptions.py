"""
サービスレイヤーの例外定義

このモジュールには、サービスレイヤーで使用される例外クラスが定義されています。
"""

class ServiceError(Exception):
    """サービスレイヤーのベース例外クラス"""
    pass

class DocumentNotFoundError(ServiceError):
    """ドキュメントが見つからない場合の例外"""
    pass

class RevisionNotFoundError(ServiceError):
    """リビジョンが見つからない場合の例外"""
    pass

class StorageError(ServiceError):
    """ストレージ操作に関するエラー"""
    pass

class ValidationError(ServiceError):
    """データバリデーションエラー"""
    pass
