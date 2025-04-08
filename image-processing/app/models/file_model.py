from app.db import db  # Import db from app/db.py

class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)  # e.g., 'uploaded', 'processing', 'completed'
    operations = db.Column(db.JSON, nullable=True)  # Store the list of operations applied (e.g., crop, filter, watermark)
    original_size = db.Column(db.Integer, nullable=False)  # Original size of the file (in bytes)
    processed_size = db.Column(db.Integer, nullable=True)  # Size after processing (in bytes, can be None if not processed)
    processed_file_url = db.Column(db.String(255), nullable=True)  # URL for the processed file (if modified)

    def __repr__(self):
        return f'<File {self.filename}>'
    
    def to_dict(self):
        """Serialize the file model to a dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'user_id': self.user_id,
            'file_url': self.file_url,
            'status': self.status,
            'operations': self.operations,
            'original_size': self.original_size,
            'processed_size': self.processed_size,
            'processed_file_url': self.processed_file_url
        }
