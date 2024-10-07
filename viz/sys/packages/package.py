from pydantic import BaseModel


class PackageItem(BaseModel):
    package_path: str
