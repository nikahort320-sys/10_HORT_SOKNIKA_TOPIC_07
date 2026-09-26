from pydantic import BaseModel, Field

class SearchProductsInput(BaseModel):
    query: str = Field(description="Product keyword to search, e.g. 'laptop', 'mouse'")

class CheckStockInput(BaseModel):
    product_id: int = Field(gt=0, description="Positive product ID integer")

class DeleteProductInput(BaseModel):
    product_id: int = Field(gt=0, description="Positive product ID integer")