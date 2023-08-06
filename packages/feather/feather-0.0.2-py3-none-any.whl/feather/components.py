#------------------------------------------------------------------------------
# Feather SDK
# Proprietary and confidential
# Unauthorized copying of this file, via any medium is strictly prohibited
# 
# (c) Feather - All rights reserved
#------------------------------------------------------------------------------
import uuid
import json
from typing import Callable, Dict, List
from feather import helpers
import base64
import numpy

# Given a list of outputs generated from a Step, generate the output data.
# Since a step may output components, we actually need the data from the components
def step_output_adapter(outputs):
    if outputs == None:
        return []

    ret = []
    for output in outputs:
        if isinstance(output, FeatherComponent):
            ret.append(output.component._serialize_payload())
        else:
            ret.append(output)
    return ret

# Given a list of inputs for a Step and input payloads as sent from an external souce,
# load the external data (input payloads) into the correct input components
def step_input_adapter(step_inputs, input_payloads):
    for idx, input in enumerate(step_inputs):
        if isinstance(input, FeatherComponent):
            if input.component.wants_data():
                payload = input_payloads.pop(0)
                input.component._inject_payload(payload) #  Will throw if not valid
            else:
                input.component.generate_payload()
        else:
            payload = input_payloads.pop(0)
            if "value" not in payload:
                raise TypeError("Input {0} has no 'value' field".format(idx))
            step_inputs[idx] = payload["value"]

class FeatherComponent:
    def  __init__(self):
        ""
        
# Base class for a Component        
class Component:
    def __init__(self, version:str, typename:str, data_source:Callable):
        self.id = str(uuid.uuid4())
        self.dataSource = data_source
        self.version = version
        if typename == None or type(typename) != str or len(typename) == 0:
            raise ValueError("Invalid typename:", typename)
        self.typename = typename

    # Serialize the component into a JSON object for saving/transmitting.
    def _serialize_schema(self, metadata:helpers.JsonObject):
        if type(self.id) != str:
            raise ValueError("Component ID should be a string - did you change it?") 
        metadata.type = "COMPONENT"
        metadata.component_type = self.typename
        metadata.version = self.version
        metadata.props = helpers.JsonObject()
        metadata.props = self.props

    #  Deserialize a component froma JSON string that was generated from a serialize call
    def deserialize(self, src:helpers.JsonObject):
        self.type = src.type
        self.version = src.version
        self.props = src.props

    # Wants data is true if the component needs external data to generate a result.
    def wants_data(self):
        return self.dataSource == None

    def generate_payload(self):
        if self.dataSource == None:
            raise ValueError("Component", self.typename, self.id,"call to generate_payload but no data_source provided")
        self.payload = self.dataSource(self)

    # Inject payload is called when data is received from an external source for this component
    def _inject_payload(self, src:helpers.JsonObject):
        ""
        #print(self.typename, self.id, ": Injecting payload", src)
        #if src.id != str(self.id):
        #    raise ValueError("Component(",str(self.id),") inject_payload wrong ID!", src.id)


##-----------------------------------------------------------------------------
## FILE LOADER
##-----------------------------------------------------------------------------
class FileLoader(Component):
    COMPONENT_ID = "File.Upload"
    COMPONENT_VERSION = "1.0.0"
    
    def __init__(self, types: List[str],
                        title: str, 
                        description: str, 
                        min_files: int, 
                        max_files: int):
        Component.__init__(self, version=FileLoader.COMPONENT_VERSION, typename=FileLoader.COMPONENT_ID, data_source=None)
        for ft in types:
            if helpers.isValidFileType(ft) == False:
                raise TypeError("File.Upload - unsupported file type '{0}'", ft)

        self.files = []
        self.props = helpers.JsonObject()
        self.props.types = types
        self.props.title = title
        self.props.description = description
        self.props.min_files = min_files
        self.props.max_files = max_files
        
    def _serialize_payload(self):
        ret = {}
        files = []
        for file in self.files:
            item = {}
            item["name"] = file.name
            item["data"] = base64.b64encode(file.data).decode("ascii")
            files.append(item)
        ret["files"] = files
        return ret

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.files = []
        for finfo in src["files"]:
            f = helpers.JsonObject()
            f.name = finfo["name"]
            f.data = base64.b64decode(finfo["data"])
            self.files.append(f)

    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.files = []
        f = helpers.JsonObject()
        f.name = "string"
        f.data = "b64"
        o.files.append(f)
        return o.toJSON(pretty=False)

    # Generate payload is called when the component is in automatic mode
    def generate_payload(self):
        Component.generate_payload(self)
        self.files = self.dataSource(self)

##-----------------------------------------------------------------------------
## FILE DOWNLOAD
##-----------------------------------------------------------------------------
class FileDownload(Component):
    COMPONENT_ID = "File.Download"
    COMPONENT_VERSION = "1.0.0"
    
    def __init__(self, files, 
                        output_filenames: List[str],
                        title: str, 
                        description: str):
        Component.__init__(self, version=FileDownload.COMPONENT_VERSION, typename=FileDownload.COMPONENT_ID, data_source=None)

        if files == None or isinstance(files, list) == False:
            raise TypeError("File.Download - 'files' must be set to a list of files, but got {0}".format(type(files)))
        self.files = files
        self.props = helpers.JsonObject()
        self.props.output_filenames = output_filenames or []
        self.props.title = title
        self.props.description = description
        
    def _serialize_payload(self):
        ret = {}
        files = []
        for file in self.files:
            item = {}
            if type(file)==bytes:
                item["name"] = ""
                item["data"] = base64.b64encode(file).decode("ascii")
            if type(file)==str:
                item["name"] = ""
                item["data"] = base64.b64encode(str.encode(file)).decode("ascii")
            else:
                item["name"] = file.name
                item["data"] = base64.b64encode(file.data).decode("ascii")
            files.append(item)
        ret["files"] = files
        return ret

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.files = []
        for finfo in src["files"]:
            f = helpers.JsonObject()
            f.name = finfo["name"]
            f.data = base64.b64decode(finfo["data"])
            self.files.append(f)

    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.files = []
        f = helpers.JsonObject()
        f.name = "string"
        f.data = "b64"
        o.files.append(f)
        return o.toJSON(pretty=False)

    # Generate payload is called when the component is in automatic mode
    def generate_payload(self):
        Component.generate_payload(self)
        self.files = self.dataSource(self)


##-----------------------------------------------------------------------------
## TEXT BOX INPUT
##-----------------------------------------------------------------------------
class TextBoxInput(Component):
    COMPONENT_ID = "Text.In"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, defaults,
                        title: str,
                        description: str,
                        num_inputs: int,
                        max_chars):

        Component.__init__(self, version=TextBoxInput.COMPONENT_VERSION, typename=TextBoxInput.COMPONENT_ID, data_source=None)
        self.text:str = None
        self.props = helpers.JsonObject()
        self.props.defaults = defaults
        self.props.title = title
        self.props.description = description
        self.props.num_inputs = num_inputs
        self.props.max_chars = max_chars

    # Inject payload is called when data is received from an external source for this component
    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.text = src["text"]
    
    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.text = []
        o.text.append("string")
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        ret["text"] = self.text
        return ret

##-----------------------------------------------------------------------------
## TEXT LABEL
##-----------------------------------------------------------------------------
class TextLabel(Component):
    COMPONENT_ID = "Text.View"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, text, title: str):

        Component.__init__(self, version=TextLabel.COMPONENT_VERSION, typename=TextLabel.COMPONENT_ID, data_source=None)
        self.text:str = text
        self.props = helpers.JsonObject()
        self.props.title = title

    # Inject payload is called when data is received from an external source for this component
    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.text = src["text"]
    
    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.text = "string"
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        ret["text"] = self.text
        return ret

##-----------------------------------------------------------------------------
## SINGLE SELECT LIST
##-----------------------------------------------------------------------------
class SingleSelectList(Component):
    COMPONENT_ID = "List.SelectOne"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, listItems: List[str],
                        title: str,
                        description: str,
                        style: str):

        Component.__init__(self, version=SingleSelectList.COMPONENT_VERSION, typename=SingleSelectList.COMPONENT_ID, data_source=None)
        if style != "dropdown" and style != "radio":
            raise ValueError("List.SelectOne style must be either 'dropdown' or 'radio'")
        if listItems == None or isinstance(listItems, list) == False:
            raise TypeError("List.SelectOne - 'listItems' must be set to a list of strings, but got {0}".format(type(listItems)))

        self.items = listItems
        self.selected_index = -1
        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description
        self.props.style = style

    # Inject payload is called when data is received from an external source for this component
    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        # Validate
        self.items = src["items"]
        self.selected_index = src["selected_index"]
    
    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.items = []
        o.items.append("string")
        o.selected_index = "int"
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        ret["items"] = self.items
        ret["selected_index"] = self.selected_index
        return ret

##-----------------------------------------------------------------------------
## MULTI SELECT LIST
##-----------------------------------------------------------------------------
class MultiSelectList(Component):
    COMPONENT_ID = "List.SelectMulti"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, listItems,
                        title: str,
                        description: str):

        Component.__init__(self, version=MultiSelectList.COMPONENT_VERSION, typename=MultiSelectList.COMPONENT_ID, data_source=None)
        if listItems == None or isinstance(listItems, list) == False:
            raise TypeError("List.SelectOne - 'listItems' must be set to a list of strings or list of tuples, but got {0}".format(type(listItems)))

        self.items = []
        for i in listItems:
            if type(i) == str:
                self.items.append((i, False))
            if type(i) == tuple:
                if len(i) != 2:
                    raise TypeError("List.SelectOne - 'listItems' tuples must have 2 items [str,bool]")
                if type(i[0]) != str or type(i[1]) != bool:
                    raise TypeError("List.SelectOne - 'listItems' tuples must be [str,bool]")
                self.items.append(i)
                continue
            raise TypeError("List.SelectOne - 'listItems' must be str[] or tuple[], but got {0}".format(type(i)))

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    # Inject payload is called when data is received from an external source for this component
    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.items = []
        for srcItem in src["items"]:
            i = srcItem["item"]
            b = srcItem["selected"]
            self.items.append((i,b))
    
    # Return the JSON schema for the payload format to inject in this component
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        o.items = []
        i = helpers.JsonObject()
        i.item = "string"
        i.selected = "bool"
        o.items.append(i)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        items = []
        for srcItems in self.items:
            i = srcItems[0]
            b = srcItems[1]
            items.append({"item": i, "selected": b})    
        ret["items"] = items
        return ret


##-----------------------------------------------------------------------------
## IMAGE WITH SINGLE SELECT
##-----------------------------------------------------------------------------
class ImageWithSingleSelect(Component):
    COMPONENT_ID = "Image.WithSelectOne"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, images, lists,
                        title: str,
                        description: str,
                        style: str):

        Component.__init__(self, version=ImageWithSingleSelect.COMPONENT_VERSION, typename=ImageWithSingleSelect.COMPONENT_ID, data_source=None)
        if isinstance(images, numpy.ndarray):
            images = [{"name":None, "image":images}]

        if style != "dropdown" and style != "radio":
            raise ValueError("Image.WithSelectOne style must be either 'dropdown' or 'radio'")
        if images == None:
            raise TypeError("Image.WithSelectOne - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))
        if len(lists) != len(images):
            raise TypeError("Image.WithSelectOne - 'lists' and 'images' must have the same length")

        self.images = []
        self.attributes = []
        self.selected_indices = []
        for l in lists:
            if type(l) != list:
                raise TypeError("Image.WithSelectOne - 'lists' must be array of array List[List[str]]")
            self.attributes.append(l)
            self.selected_indices.append(-1)

        if type(images) is list:
            for obj in images:
                if type(obj) != dict:
                    raise TypeError("Image.WithSelectOne - 'images' must be List[object] - got {0}".format(type(obj)))
                if "name" not in obj:
                    raise TypeError("Image.WithSelectOne - 'images' - missing 'name' attribute")
                if "image" not in obj:
                    raise TypeError("Image.WithSelectOne - 'images' - missing 'image' attribute")

                if isinstance(obj["image"], numpy.ndarray) == False:
                    raise TypeError("Image.WithSelectOne - 'One or more images is not a numpy array")
                self.images.append(obj)
        else:
            raise TypeError("Image.WithSelectOne - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description
        self.props.style = style

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.images = []
        self.attributes = []
        self.selected_indices = []

        for im in src["images"]:
            if "data" not in im:
                raise ValueError("Image.WithSelectOne - no 'data' field in 'images' list")
            if "name" not in im:
                raise ValueError("Image.WithSelectOne - no 'name' field in 'images' list")
            data = im["data"]
            name = im["name"]
            selected = im["selected_index"]
            attributes = im["attributes"]
            # TODO Validate
            self.images.append({"image": numpy.array(data), "name": name})
            self.attributes.append(attributes)
            self.selected_indices.append(selected)
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        im = helpers.JsonObject()
        im.data = "numpy"
        im.name = "string"
        im.attributes = ["string"]
        im.selected_index = "int"
        o.images = []
        o.images.append(im)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        images = []
        for idx in range(len(self.images)):
            image = self.images[idx]
            attributes = self.attributes[idx]
            selected = self.selected_indices[idx]
            obj = {}
            obj["data"] = image["image"].tolist()
            obj["name"] = image["name"]
            obj["attributes"] = attributes
            obj["selected_index"] = selected
            images.append(obj)
        ret["images"] = images
        return ret

##-----------------------------------------------------------------------------
## IMAGE WITH MULTI SELECT
##-----------------------------------------------------------------------------
class ImageWithMultiSelect(Component):
    COMPONENT_ID = "Image.WithSelectMulti"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, images, lists,
                        title: str,
                        description: str):

        Component.__init__(self, version=ImageWithMultiSelect.COMPONENT_VERSION, typename=ImageWithMultiSelect.COMPONENT_ID, data_source=None)
        if isinstance(images, numpy.ndarray):
            images = [{"name":None, "image":images}]

        if len(lists) != len(images):
            raise TypeError("Image.WithSelectMulti - 'lists' and 'images' must have the same length {0} != {1}".format(len(lists), len(images)))

        self.images = []
        self.attributes = []
        for l in lists:
            if type(l) != list:
                raise TypeError("Image.WithSelectMulti - 'lists' must be array of array List[List[str]] or List[List[Tuple]]")
            innerList = []
            for li in l:
                if type(li) is tuple:
                    if type(li[0]) != str or type(li[1]) != bool or len(li) != 2:
                        raise TypeError("Image.WithSelectMulti - 'lists' should be a List[List[Tuple(str, bool)]]")
                    innerList.append(li)
                elif type(li) is str:
                    innerList.append((li, False))
            self.attributes.append(innerList)

        if type(images) is list:
            for obj in images:
                if type(obj) != dict:
                    raise TypeError("Image.WithSelectMulti - 'images' must be List[{name, image}]")
                if "name" not  in obj:
                    raise TypeError("Image.WithSelectMulti - 'images' - missing 'name' attribute")
                if "image" not  in obj:
                    raise TypeError("Image.WithSelectMulti - 'images' - missing 'image' attribute")

                if isinstance(obj["image"], numpy.ndarray) == False:
                    raise TypeError("Image.WithSelectMulti - 'One or more images is not a numpy array")
                self.images.append(obj)
        else:
            raise TypeError("Image.WithSelectMulti - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.images = []
        self.attributes = []

        for im in src["images"]:
            if "data" not in im:
                raise ValueError("Image.WithSelectMulti - no 'data' field in 'images' list")
            if "name" not in im:
                raise ValueError("Image.WithSelectMulti - no 'name' field in 'images' list")
            data = im["data"]
            name = im["name"]
            attributes = im["attributes"]
            # TODO Validate
            self.images.append({"image": numpy.array(data), "name": name})
            outList = []
            for attr in attributes:
                outList.append((attr["text"], attr["selected"]))
            self.attributes.append(outList)
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        im = helpers.JsonObject()
        im.data = "numpy"
        im.name = "string"
        attr = helpers.JsonObject()
        attr.selected = "bool"
        attr.text = "string"
        im.attributes = [attr]
        o.images = []
        o.images.append(im)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        images = []
        for idx in range(len(self.images)):
            image = self.images[idx]
            attributes = []
            for a in self.attributes[idx]:
                # Attributes are a list of a list of Tuples (we normalize in the constructor)
                innerObj = {}
                innerObj["text"] = a[0]
                innerObj["selected"] = a[1]
                attributes.append(innerObj)
            obj = {}
            obj["data"] = image["image"].tolist()
            obj["name"] = image["name"]
            obj["attributes"] = attributes
            images.append(obj)
        ret["images"] = images
        return ret

##-----------------------------------------------------------------------------
## IMAGE WITH TEXT
##-----------------------------------------------------------------------------
class ImageWithText(Component):
    COMPONENT_ID = "Image.WithText"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, images, text,
                        title: str,
                        description: str):

        Component.__init__(self, version=ImageWithText.COMPONENT_VERSION, typename=ImageWithText.COMPONENT_ID, data_source=None)
        if isinstance(images, numpy.ndarray):
            images = [images]

        if images == None:
            raise TypeError("Image.WithText - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))
        if len(text) != len(images):
            raise TypeError("Image.WithText - 'text' and 'images' must have the same length")

        self.images = []
        self.text = []
        for l in text:
            if type(l) != str:
                raise TypeError("Image.WithText - 'text' must be array of array List[str]")
            self.text.append(l)

        if type(images) is list:
            for im in images:
                if isinstance(im, numpy.ndarray) == False:
                    raise TypeError("Image.WithText - 'One or more images is not a numpy array")
                self.images.append(im)
        else:
            raise TypeError("Image.WithText - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.images = []
        self.text = []

        for im in src["images"]:
            data = im["data"]
            # TODO Validate
            self.images.append(numpy.array(data))
            self.text.append(im["text"])
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        im = helpers.JsonObject()
        im.data = "numpy"
        im.text = "string"
        o.images = []
        o.images.append(im)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        images = []
        for idx in range(len(self.images)):
            image = self.images[idx]
            obj = {}
            obj["data"] = image.tolist()
            obj["text"] = self.text[idx]
            images.append(obj)
        ret["images"] = images
        return ret

##-----------------------------------------------------------------------------
## IMAGE VIEW
##-----------------------------------------------------------------------------
class ImageView(Component):
    COMPONENT_ID = "Image.View"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, images, output_text,
                        title: str,
                        description: str):

        Component.__init__(self, version=ImageView.COMPONENT_VERSION, typename=ImageView.COMPONENT_ID, data_source=None)
        if isinstance(images, numpy.ndarray):
            images = [images]

        if images == None:
            raise TypeError("Image.View - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))
        if len(output_text) != len(images):
            raise TypeError("Image.View - 'output_text' and 'images' must have the same length")

        self.images = []
        self.text = []
        for l in output_text:
            if type(l) != str:
                raise TypeError("Image.View - 'output_text' must be array of array List[str]")
            self.text.append(l)

        if type(images) is list:
            for im in images:
                if isinstance(im, numpy.ndarray) == False:
                    raise TypeError("Image.View - 'One or more images is not a numpy array")
                self.images.append(im)
        else:
            raise TypeError("Image.View - 'images' must be set to a numpy[], or List[numpy[]], but got {0}".format(type(images)))

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.images = []
        self.text = []

        for im in src["images"]:
            data = im["data"]
            # TODO Validate
            self.images.append(numpy.array(data))
            self.text.append(im["text"])
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        im = helpers.JsonObject()
        im.data = "numpy"
        im.text = "string"
        o.images = []
        o.images.append(im)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        images = []
        for idx in range(len(self.images)):
            image = self.images[idx]
            obj = {}
            obj["data"] = image.tolist()
            obj["text"] = self.text[idx]
            images.append(obj)
        ret["images"] = images
        return ret

##-----------------------------------------------------------------------------
## DOCUMENT VIEW
##-----------------------------------------------------------------------------
class DocumentView(Component):
    COMPONENT_ID = "Document.View"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, documents, text,
                        title: str,
                        description: str):

        Component.__init__(self, version=DocumentView.COMPONENT_VERSION, typename=DocumentView.COMPONENT_ID, data_source=None)

        if documents == None:
            raise TypeError("Document.View - 'documents' must be set")
        
        if text != None and len(documents) != len(text):
            raise TypeError("Document.View - 'documents' and 'text' must have the same length")

        self.documents = []
        self.text = []
        for d in documents:
            if type(d) == str:
                self.documents.append({"name":None, "document":d})
            else:
                self.documents.append({"name":d["name"], "document": d["document"]})

        for t in text:
            if type(t) != str:
                raise TypeError("Document.View -  elements of 'text' must be strings - got {0}".format(type(t)))
            self.text.append(t)

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.documents = []
        self.text = []

        for im in src["documents"]:
            self.documents.append({"document": im["document"], "name": im["name"]})
            self.text.append(im["text"])
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        doc = helpers.JsonObject()
        doc.document = "string"
        doc.text = "string"
        doc.name = "string"
        o.documents = []
        o.documents.append(doc)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        documents = []
        for idx in range(len(self.documents)):
            obj = {}
            obj["document"] = self.documents[idx]["document"]
            obj["name"] = self.documents[idx]["name"]
            obj["text"] = self.text[idx]
            documents.append(obj)
        ret["documents"] = documents
        return ret

##-----------------------------------------------------------------------------
## DOCUMENT WITH TEXT
##-----------------------------------------------------------------------------
class DocumentWithText(Component):
    COMPONENT_ID = "Document.WithText"
    COMPONENT_VERSION = "1.0.0"

    def __init__(self, documents, text,
                        title: str,
                        description: str):

        Component.__init__(self, version=DocumentWithText.COMPONENT_VERSION, typename=DocumentWithText.COMPONENT_ID, data_source=None)

        if documents == None:
            raise TypeError("Document.WithText - 'documents' must be set")
        
        if text != None and len(documents) != len(text):
            raise TypeError("Document.WithText - 'documents' and 'text' must have the same length")

        self.documents = []
        self.text = []
        for d in documents:
            if type(d) == str:
                self.documents.append({"name":None, "document":d})
            else:
                self.documents.append({"name":d["name"], "document": d["document"]})

        for t in text:
            if type(t) != str:
                raise TypeError("Document.WithText -  elements of 'text' must be strings - got {0}".format(type(t)))
            self.text.append(t)

        self.props = helpers.JsonObject()
        self.props.title = title
        self.props.description = description

    def _inject_payload(self, src:helpers.JsonObject):
        Component._inject_payload(self, src)
        self.documents = []
        self.text = []

        for im in src["documents"]:
            self.documents.append({"document": im["document"], "name": im["name"]})
            self.text.append(im["text"])
    
    def _get_payload_schema(self):
        o = helpers.JsonObject()
        doc = helpers.JsonObject()
        doc.document = "string"
        doc.text = "string"
        doc.name = "string"
        o.documents = []
        o.documents.append(doc)
        return o.toJSON(pretty=False)

    def _serialize_payload(self):
        ret = {}
        documents = []
        for idx in range(len(self.documents)):
            obj = {}
            obj["document"] = self.documents[idx]["document"]
            obj["name"] = self.documents[idx]["name"]
            obj["text"] = self.text[idx]
            documents.append(obj)
        ret["documents"] = documents
        return ret
