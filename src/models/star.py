# star.py (backend models)

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List
from datetime import datetime
import datetime as dt
import math
import uuid

class Star(BaseModel):
    """Star model representing a star in the sky map"""
    id: Optional[str] = None
    x: float
    y: float
    message: str
    last_liked: Optional[float] = None
    creation_date: Optional[float] = None
    user_id: Optional[str] = None
    username: Optional[str] = None

    @field_validator('x', 'y')
    def validate_coordinates(cls, v):
        # if not -1 <= v <= 1:
        #     raise ValueError('Coordinates must be between -1 and 1')
        return v

    @field_validator('message')
    def validate_message(cls, v):
        if len(v) > 256:  # Twitter-style limit
            raise ValueError('Message too long')
        return v
        
    def to_entity(self):
        """Convert the Star model to an Azure Table entity"""
        current_time = datetime.now().timestamp()
        return {
            "PartitionKey": f"STAR_{datetime.now().strftime('%Y%m')}",
            "RowKey": self.id or str(uuid.uuid4()),
            "X": self.x,
            "Y": self.y,
            "Message": self.message,
            "LastLiked": self.last_liked or current_time,
            "creationDate": self.creation_date or current_time,
            "UserId": self.user_id,
            "Username": self.username
        }
    
    @classmethod
    def from_entity(cls, entity: Dict) -> "Star":
        """Create star model from Azure table entity"""
        return cls(
            id=entity["RowKey"],
            x=entity["X"],
            y=entity["Y"],
            message=entity["Message"],
            last_liked=entity.get("LastLiked"),
            creation_date=entity.get("creationDate"),
            user_id=entity.get("UserId"),
            username=entity.get("Username")
        )

# def calculate_current_brightness(base_brightness: float, last_liked: float) -> float:
#     """Calculate the current brightness based on time decay"""
#     time_since_liked = datetime.now(dt.timezone.utc).timestamp() - last_liked
#     decay_factor = max(0.01, 1.0 - 0.01 * time_since_liked)
#     return max(20.0, base_brightness * math.exp(-decay_factor * time_since_liked))
