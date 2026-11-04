from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Impostazioni generali dell'applicazione, lette dall'ambiente (.env)."""

    cors_origins: str = "http://localhost:5173"


settings = Settings()


class Statuto(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STATUTO_")
    scadenza_risposta_giorni: int = 60
    quorum_direttivo: int = 4
    max_membri_direttivo: int = 7
    mesi_per_voto_assemblea: int = 3
    durata_quota_mesi: int = 12


statuto = Statuto()
