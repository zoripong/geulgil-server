# coding: utf-8
# db = SQLAlchemy()
from geulgil import db  # TODO TEST


class Mean(db.Model):
    __tablename__ = 'mean'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.ForeignKey('word.id'), nullable=False, index=True)
    mean = db.Column(db.Text, nullable=False)

    word = db.relationship('Word',
                           primaryjoin='Mean.word_id == Word.id',
                           backref='means')


class MeanKeyword(db.Model):
    __tablename__ = 'mean_keywords'

    id = db.Column(db.Integer, primary_key=True)
    mean_id = db.Column(db.ForeignKey('mean.id'), nullable=False, index=True)
    mean_keyword = db.Column(db.String(50), nullable=False)

    mean = db.relationship('Mean',
                           primaryjoin='MeanKeyword.mean_id == Mean.id',
                           backref='mean_keywords')


class SimilarKeyword(db.Model):
    __tablename__ = 'similar_keywords'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.ForeignKey('word.id'), nullable=False, index=True)
    similar_keyword = db.Column(db.String(50), nullable=False)

    word = db.relationship('Word',
                           primaryjoin='SimilarKeyword.word_id == Word.id',
                           backref='similar_keywords')


class Word(db.Model):
    __tablename__ = 'word'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    part = db.Column(db.Integer,
                     nullable=False,
                     server_default=db.FetchedValue())
