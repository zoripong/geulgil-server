# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Mean(db.Model):
    __tablename__ = 'mean'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.ForeignKey('word.id'), nullable=False, index=True)
    mean = db.Column(db.Text, nullable=False)

    word = db.relationship('Word', primaryjoin='Mean.word_id == Word.id', backref='means')


class MeanKeyword(db.Model):
    __tablename__ = 'mean_keywords'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.ForeignKey('word.id'), nullable=False, index=True)
    mean_keyword = db.Column(db.String(50), nullable=False)

    word = db.relationship('Word', primaryjoin='MeanKeyword.word_id == Word.id', backref='mean_keywords')


class SimilarKeyword(db.Model):
    __tablename__ = 'similar_keywords'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.ForeignKey('word.id'), nullable=False, index=True)
    similar_keyword = db.Column(db.String(50), nullable=False)

    word = db.relationship('Word', primaryjoin='SimilarKeyword.word_id == Word.id', backref='similar_keywords')


class Word(db.Model):
    __tablename__ = 'word'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
