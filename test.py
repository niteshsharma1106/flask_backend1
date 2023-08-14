from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create a SQLite database in memory (you can change this to a file path)
engine = create_engine('sqlite:///database1.db')
Base = declarative_base()
db = SQLAlchemy()

class Cluster(Base):
    __tablename__ = 'cluster'
    
    id = Column(Integer, primary_key=True)
    clusterapi = db.Column(db.String(200),unique=True,nullable=False)
    dctype = db.Column(db.String(200),nullable=False)
    dcloc = db.Column(db.String(200),nullable=False)
    ctype = db.Column(db.String(200),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tridents = db.relationship('Trident', back_populates='cluster')

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Trident(Base):
    __tablename__ = 'trident'
    
    id = Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
    svmname = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    cluster = db.relationship('Cluster', back_populates='tridents')

Base.metadata.create_all(engine)

# Example usage
Session = sessionmaker(bind=engine)
session = Session()

new_cluster = Cluster(clusterapi='api_key', dctype='type', dcloc='location', type='cluster_type')
new_trident = Trident(user_id=new_cluster.id, svmname='svm_name')
new_cluster.tridents.append(new_trident)
session.add(new_cluster)
session.commit()


new_cluster1 = Cluster(clusterapi='api_key2', dctype='type2', dcloc='location2', type='cluster_type2')
new_trident1 = Trident(user_id=new_cluster.id, svmname='svm_name2')
new_cluster1.tridents.append(new_trident1)
session.add(new_cluster1)
session.commit()


session.close()
