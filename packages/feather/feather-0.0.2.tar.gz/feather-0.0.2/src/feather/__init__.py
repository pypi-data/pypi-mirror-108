#------------------------------------------------------------------------------
# Feather SDK
# Proprietary and confidential
# Unauthorized copying of this file, via any medium is strictly prohibited
# 
# (c) Feather - All rights reserved
#------------------------------------------------------------------------------
import typing
from feather.featherlocal import webserver, systemrunner, publisher
from typing import Callable, List
from feather import components
from feather.helpers import JsonObject
import os

def build(name, bootstrap: Callable, steps: List[Callable], 
    description="", deploy=False, interactive=True, file_bundle=None):
    """Build and optionally deploy a system to the feather service"""

    if os.environ.get("FEATHER_SERVICE_RUNNER") != None:
        raise RuntimeError("Calling ftr.Build from Runner")
        
    if bootstrap == None:
        raise ValueError("Bootstrap must be set to a valid init function")

    # Validate args
    if steps == None:
        raise ValueError("'None' steps provided")

    if len(steps) == 0:
        raise ValueError("No steps provided - you must provide at least 1 step")

    runner = systemrunner.SystemRunner(name, description, bootstrap=bootstrap, steps=steps, file_bundle=file_bundle)

    if interactive == True:
        webserver.start_server()
        webserver.new_system(runner)
    else:    
        runner.run_to_completion()
        runner.serialize(final=True)
        print(runner.schema.toJSON())
        if deploy == True:
            # NOTE: Test Only, not for production
            runner.publish(api_key="aca5d56b-81fd-4704-9e83-46b85628bdb0")
    return runner.finalOutputs

# Decorators
def step(title: str, description: str = None):
    def decorator(func):
        func._ftr_title = title
        func._ftr_description = description
        return func
    return decorator


# Public Bundle API

def bundle(code_files, model_files=[]):
    ret = publisher.Bundle(code_files)
    return ret
    
# Public Components API

class File:
    class Upload(components.FeatherComponent):
        def __init__(self, types: List[str],
                        title: str = None, 
                        description: str = None, 
                        min_files: int = 1, 
                        max_files: int = 1):
            self.component = components.FileLoader(types=types, title=title, description=description, 
                                                    min_files=min_files, max_files=max_files)
                
        def get_files(self):
            return self.component.files


    class Download(components.FeatherComponent):
        def __init__(self, files,
                        title: str = None,
                        description: str = None, 
                        output_filenames: List[str] = None):
            self.component = components.FileDownload(files=files, output_filenames=output_filenames, title=title, description=description)

class Text:
    class In(components.FeatherComponent):
        def __init__(self, defaults,
                        title: str = None,
                        description: str = None,
                        num_inputs: int = 1,
                        max_chars = None):
            self.component = components.TextBoxInput(defaults=defaults, title=title, description=description,
                                                    num_inputs=num_inputs, max_chars=max_chars)

        def get_text(self):
            return self.component.text

    class View(components.FeatherComponent):
        def __init__(self, text: str,
                        title: str = None):
            self.component = components.TextLabel(text=text, title=title)

class List:
    class SelectOne(components.FeatherComponent):
        def __init__(self, items: List[str],
                        title: str = None,
                        description: str = None,
                        style: str = "dropdown"):
            self.component = components.SingleSelectList(listItems=items, title=title, description=description, style=style)

    class SelectMulti(components.FeatherComponent):
        def __init__(self, items,
                        title: str = None,
                        description: str = None):
            self.component = components.MultiSelectList(listItems=items, title=title, description=description)

class Image:
    class WithSelectOne(components.FeatherComponent):
        def __init__(self, images, lists: typing.List[typing.List[str]],
                        title: str = None,
                        description: str = None,
                        style: str = "radio"):
            self.component = components.ImageWithSingleSelect(images=images, lists=lists, title=title, description=description, style=style)

    class WithSelectMulti(components.FeatherComponent):
        def __init__(self, images, lists,
                        title: str = None,
                        description: str = None):
            self.component = components.ImageWithMultiSelect(images=images, lists=lists, title=title, description=description)

    class WithText(components.FeatherComponent):
        def __init__(self, images,
                        title: str = None,
                        description: str = None,
                        text: typing.List[str] = None):
            self.component = components.ImageWithText(images=images, text=text, title=title, description=description)

    class View(components.FeatherComponent):
        def __init__(self, images,
                        title: str = None,
                        description: str = None,
                        output_text: typing.List[str] = None):
            self.component = components.ImageView(images=images, output_text=output_text, title=title, description=description)
            

class Document(components.FeatherComponent):
    class WithText(components.FeatherComponent):
        def __init__(self, documents, 
                        title: str = None,
                        description: str = None,
                        output_text: typing.List[str] = None):
            self.component = components.DocumentWithText(documents=documents, text=output_text, title=title, description=description)

    class View(components.FeatherComponent):
        def __init__(self, documents,
                        title: str = None,
                        description: str = None,
                        output_text: typing.List[str] = None):
            self.component = components.DocumentView(documents=documents, text=output_text, title=title, description=description)
