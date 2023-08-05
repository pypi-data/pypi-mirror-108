![simplet5](data/simplet5.png)


<h3 style="text-align:center; font-weight: bold">
 Quickly train T5 models in just 3 lines of code + ONNX support
</h3>

**simpleT5** is built on top of PyTorch-lightning⚡️ and Transformers🤗 that lets you quickly train your T5 models.
> T5 models can be used for several NLP tasks such as summarization, QA, QG, translation, text generation, and more. 

## Install
```python
pip install --upgrade simplet5
```


## Usage
```python
# import
from simplet5 import SimpleT5

# instantiate
model = SimpleT5()

# load
model.from_pretrained("t5","t5-base")

# train
model.train(train_df=train_df, # pandas dataframe with 2 columns: source_text & target_text
            eval_df=eval_df, # pandas dataframe with 2 columns: source_text & target_text
            source_max_token_len = 512, 
            target_max_token_len = 128,
            batch_size = 8,
            max_epochs = 5,
            use_gpu = True,
            outputdir = "outputs",
            early_stopping_patience_epochs = 0
            )

# load trained T5 model
model.load_model("t5","path/to/trained/model/directory", use_gpu=False)

# predict
model.predict("input text for prediction")

# need faster inference on CPU, get ONNX support
model.convert_and_load_onnx_model("path/to/T5 model/directory")
model.onnx_predict("input text for prediction")

```




