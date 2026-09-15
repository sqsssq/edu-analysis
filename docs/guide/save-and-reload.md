# Save and reload

Fitted models can be saved with their preprocessing contract and loaded later:

```python
model.save("artifacts/model.pt")
reloaded = LearningModel.load("artifacts/model.pt")
prediction = reloaded.predict(new_table)
```

The artifact stores parameters, feature order, thresholds, metadata, and quality
evidence. It does not store raw input rows. Treat artifacts built from restricted
research data as local files unless their contents have been reviewed.
