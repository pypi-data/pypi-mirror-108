# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nucleus']

package_data = \
{'': ['*']}

install_requires = \
['grequests>=0.6.0,<0.7.0', 'requests>=2.25.1,<3.0.0', 'tqdm>=4.41.0,<5.0.0']

extras_require = \
{':python_version >= "3.6.1" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'scale-nucleus',
    'version': '0.1.6',
    'description': 'The official Python client library for Nucleus, the Data Platform for AI',
    'long_description': '# Nucleus\n\nhttps://dashboard.scale.com/nucleus\n\nAggregate metrics in ML are not good enough. To improve production ML, you need to understand their qualitative failure modes, fix them by gathering more data, and curate diverse scenarios.\n\nScale Nucleus helps you:\n\n* Visualize your data\n* Curate interesting slices within your dataset\n* Review and manage annotations\n* Measure and debug your model performance\n\nNucleus is a new way—the right way—to develop ML models, helping us move away from the concept of one dataset and towards a paradigm of collections of scenarios.\n\n\n\n## Installation\n\n`$ pip install scale-nucleus`\n\n## Usage\n\nThe first step to using the Nucleus library is instantiating a client object.\nThe client abstractions serves to authenticate the user and act as the gateway\nfor users to interact with their datasets, models, and model runs.\n\n### Create a client object\n```python\nimport nucleus\nclient = nucleus.NucleusClient("YOUR_API_KEY_HERE")\n```\n\n### Create Dataset\n```python\ndataset = client.create_dataset("My Dataset")\n```\n\n### List Datasets\n```python\ndatasets = client.list_datasets()\n```\n\n### Delete a Dataset\nBy specifying target dataset id.\nA response code of 200 indicates successful deletion.\n```python\nclient.delete_dataset("YOUR_DATASET_ID")\n```\n\n### Append Items to a Dataset\nYou can append both local images and images from the web. Simply specify the location and Nucleus will automatically infer if it\'s remote or a local file.\n```python\ndataset_item_1 = DatasetItem(image_location="./1.jpeg", reference_id="1", metadata={"key": "value"})\ndataset_item_2 = DatasetItem(image_location="s3://srikanth-nucleus/9-1.jpg", reference_id="2", metadata={"key": "value"})\n```\n\nThe append function expects a list of `DatasetItem` objects to upload, like this:\n```python\nresponse = dataset.append([dataset_item_1, dataset_item_2])\n```\n\n### Get Dataset Info\nTells us the dataset name, number of dataset items, model_runs, and slice_ids.\n```python\ndataset.info\n```\n\n### Access Dataset Items\nThere are three methods to access individual Dataset Items:\n\n(1) Dataset Items are accessible by reference id\n```python\nitem = dataset.refloc("my_img_001.png")\n```\n(2) Dataset Items are accessible by index\n```python\nitem = dataset.iloc(0)\n```\n(3) Dataset Items are accessible by the dataset_item_id assigned internally\n```python\nitem = dataset.loc("dataset_item_id")\n```\n\n### Add Annotations\nUpload groundtruth annotations for the items in your dataset.\nBox2DAnnotation has same format as https://dashboard.scale.com/nucleus/docs/api#add-ground-truth\n```python\nannotation_1 = BoxAnnotation(reference_id="1", label="label", x=0, y=0, width=10, height=10, annotation_id="ann_1", metadata={})\nannotation_2 = BoxAnnotation(reference_id="2", label="label", x=0, y=0, width=10, height=10, annotation_id="ann_2", metadata={})\nresponse = dataset.annotate([annotation_1, annotation_2])\n```\n\nFor particularly large payloads, please reference the accompanying scripts in **references**\n\n### Add Model\nThe model abstraction is intended to represent a unique architecture.\nModels are independent of any dataset.\n\n```python\nmodel = client.add_model(name="My Model", reference_id="newest-cnn-its-new", metadata={"timestamp": "121012401"})\n```\n\n### Upload Predictions to ModelRun\nThis method populates the model_run object with predictions. `ModelRun` objects need to reference a `Dataset` that has been created.\nReturns the associated model_id, human-readable name of the run, status, and user specified metadata.\nTakes a list of Box2DPredictions within the payload, where Box2DPrediction\nis formulated as in https://dashboard.scale.com/nucleus/docs/api#upload-model-outputs\n```python\nprediction_1 = BoxPrediction(reference_id="1", label="label", x=0, y=0, width=10, height=10, annotation_id="pred_1", confidence=0.9)\nprediction_2 = BoxPrediction(reference_id="2", label="label", x=0, y=0, width=10, height=10, annotation_id="pred_2", confidence=0.2)\n\nmodel_run = model.create_run(name="My Model Run", metadata={"timestamp": "121012401"}, dataset=dataset, predictions=[prediction_1, prediction_2])\n```\n\n### Commit ModelRun\nThe commit action indicates that the user is finished uploading predictions associated\nwith this model run.  Committing a model run kicks off Nucleus internal processes\nto calculate performance metrics like IoU. After being committed, a ModelRun object becomes immutable.\n```python\nmodel_run.commit()\n```\n\n### Get ModelRun Info\nReturns the associated model_id, human-readable name of the run, status, and user specified metadata.\n```python\nmodel_run.info\n```\n\n### Accessing ModelRun Predictions\nYou can access the modelRun predictions for an individual dataset_item through three methods:\n\n(1) user specified reference_id\n```python\nmodel_run.refloc("my_img_001.png")\n```\n(2) Index\n```python\nmodel_run.iloc(0)\n```\n(3) Internally maintained dataset_item_id\n```python\nmodel_run.loc("dataset_item_id")\n```\n\n### Delete ModelRun\nDelete a model run using the target model_run_id.\n\nA response code of 200 indicates successful deletion.\n```python\nclient.delete_model_run("model_run_id")\n```\n\n## For Developers\n\nClone from github and install as editable\n\n```\ngit clone git@github.com:scaleapi/nucleus-python-client.git\ncd nucleus-python-client\npip3 install poetry\npoetry install\n```\n\nPlease install the pre-commit hooks by running the following command:\n```python\npoetry run pre-commit install\n```\n\n**Best practices for testing:**\n(1). Please run pytest from the root directory of the repo, i.e.\n```\npoetry pytest tests/test_dataset.py\n```\n\n\n',
    'author': 'Scale AI Nucleus Team',
    'author_email': 'nucleusapi@scaleapi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://scale.com/nucleus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
