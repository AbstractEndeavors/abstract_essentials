"""
Abstract Essentials - Create Module Folder

This module provides functionalities for creating a new module folder with necessary files, such as README, setup.cfg, pyproject.toml, LICENSE, source files, and more. It facilitates the creation of Python packages by generating essential configuration files and boilerplate code.

Author: putkoff
partOf: abstract_modules
Date: 05/31/2023
Version: 0.0.1.0
author_email: 'partners@abstractendeavors.com'
url: 'https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_utilities'

Dependencies:
- abstract_utilities.string_clean (eatAll)
- abstract_utilities.path_utils (mkdirs)
- abstract_utilities.read_write_utils (write_to_file, read_from_file)
- abstract_gui

Usage:
This module provides a function `create_module_folder()` that guides users through creating a new Python module folder. It interacts with the user through a GUI window, allowing them to set various configuration options for the module, including package information, classifiers, and files to create.

Example:
To create a new module folder with the provided functionalities, you can call the `create_module_folder()` function:

```python
from create_module_folder import create_module_folder

module_folder_path = create_module_folder()
print("New module folder created at:", module_folder_path)

License:
This module is provided under the MIT License. You can find the full text of the license in the 'LICENSE' file of the Abstract Essentials repository.

Contributions:
Contributions to this module are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or create a pull request on the GitHub repository.

Disclaimer:
This module is provided as-is, and the author is not responsible for any issues or consequences that may arise from its usage. Use this module at your own risk and ensure you understand its functionality before incorporating it into your projects.
"""
from abstract_utilities.string_clean import eatAll
from abstract_utilities.path_utils import mkdirs
from abstract_utilities.read_write_utils import write_to_file,read_from_file
from .module_utils import get_installed_versions,scan_folder_for_required_modules
from abstract_gui import *
import datetime
import os
import json
create_folder_window_mgr,create_folder_bridge,create_folder_script = create_window_manager(script_name='create_folder_script',global_var=globals())
def get_tag_date() -> str:
    """
    Get the current date in the format 'YYYYMMDD'.

    Returns:
        str: The current date in the format 'YYYYMMDD'.
    """
    return datetime.now().strftime('%Y%m%d')
def get_current_year() -> int:
    """
    Get the current year.

    Returns:
        int: The current year as an integer.
    """
    now = datetime.datetime.now()
    current_year = now.year
    return current_year
def clean_list(ls: list) -> list:
    """
    Clean a list by removing empty string elements.

    Args:
        ls (list): The list to be cleaned.

    Returns:
        list: A new list with empty string elements removed.
    """
    lsN=[]
    for each in ls:
        if each != '':
            lsN.append(each)
    return lsN
def create_setup_cfg() -> str:
    """
    Create the contents of a 'setup.cfg' file.

    Returns:
        str: The contents of the 'setup.cfg' file.
    """
    return f'''[bdist_wheel]
tag_build = dev
tag_date = {get_tag_date()}'''
def create_toml() -> str:
    """
    Create the contents of a 'pyproject.toml' file.

    Returns:
        str: The contents of the 'pyproject.toml' file.
    """
    return f'''[build-system]
    requires = ["{get_installed_versions(['setuptools'])}"]
    build-backend = "setuptools.build_meta"'''
def get_long_description(path: str = "README.md") -> str:
    """
    Get the contents of a long description from a file.

    Args:
        path (str): The path to the file containing the long description.
                    Default is "README.md".

    Returns:
        str: The contents of the long description.
    """
    with open(path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
def get_main_py() -> str:
    """
    Generate the contents of the 'main.py' file.

    Returns:
        str: The contents of the 'main.py' file.
    """
    return f"""import os
import importlib.util

excluded_files = ['__pycache__', 'main.py', '__init__.py']
excluded_directories = ['__pycache__']

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_filtered_files(directory):
    modules = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item not in excluded_files:
            if item_path.endswith('.py'):
                modules.append(import_module_from_file(item_path))
        elif os.path.isdir(item_path) and item not in excluded_directories:
            modules.extend(get_filtered_files(item_path))
    return modules


def main():
    print("Hello, this is {package_name}.")
    # You can import and use other modules or functions of {package_name} here.
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)

    filtered_modules = get_filtered_files(directory_path)

if __name__ == "__main__":
    # Get the absolute directory path of the current script file
    main()"""
def licenses(license,args:dict={"author_name":"name","year":str(get_current_year()),"company_name":'["Company Name"]',"jurisdiction":"[Your jurisdiction]","software_name":'("the Software")',"licensee":'("the Licensee")',"licensor":'("the Licensor")'}):
    author_name, year, company_name, jurisdiction, software_name, licensee, licensor = args.values()
    """
    Generate a license text with specified parameters.

    Args:
        license (str): The chosen license type.
        args (dict): A dictionary containing parameter values for the license text.

    Returns:
        str: The generated license text with formatted parameters.
    """
    return {"Public Domain":
     """Public Domain Dedication
========================

The author or authors of this software dedicate all their rights in this work worldwide under public domain dedication. You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.

This software is distributed without any warranty.

The author(s) are not liable for any damages, including lost profits, arising from the use of, or inability to use, this software.

You should have received a copy of the CC0 Public Domain Dedication along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.""",
     "MIT License":f"""This project is licensed under the MIT License

MIT License

The MIT License was first developed at the Massachusetts Institute of Technology (MIT) in the late 1980s. The exact origins MIT license are bit of mystery. Like the Apache 2.0, and BSD family of licenses the MIT License is a permissive software license that places few restrictions of reuse. Users of software using an MIT License are permitted to use, copy, modify, merge publish, distribute, sublicense and sell copies of the software. Some notable projects use the MIT License including Ruby on Rails, and the X Windows System.
MIT License Conditions
The MIT License is relatively simple and short. Below is the text of the MIT License from the Open Software Initiative.
Begin license text.

Copyright {year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
End license text.
Using MIT Licensed Code

 

The basic conditions of using the MIT License are:

1. The original copyright notice

2. A copy of the license itself

are including in all copies or any substantial portions of the software.
MIT License Compatibility

The MIT License is highly compatible with other permissive licenses. Including the BSD family of licenses. It is generally compatible with  GNU GPL group of licenses. However if you distribute the code that contains or is derivative of GNU GPL code the final project must of GPL compliant. In other words any source code must of publicly available. 
MIT License, Patents

The MIT License was developed before patenting software was a common practice in the U.S. It therefore does not contain an express patent license. The broad nature of the license in general, is considered by some to encompass an implicit waiver of patent rights. If you are concerned about patent rights, the Apache 2.0 license contains an explicit contributor's patent license.
MIT No Attribution License (MIT-0)

The MIT No Attribution License is a Public Domain equivalent license it is similar to the  BSD Free license. 

 
Copyright {year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files {software_name}, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

""","Proprietary/Closed Source":f"""{company_name} - Proprietary License v1.0

This software and its associated documentation {software_name} is the proprietary and confidential property of Your Company Name {licensor}. By using, accessing, or installing the Software, you ("the Licensee") agree to be bound by the terms and conditions of this license agreement ("the Agreement").

1. License Grant:
   Subject to the terms of this Agreement, the Licensor grants the Licensee a non-exclusive, non-transferable, and revocable license to use the Software for internal purposes only. The Licensee may not modify, distribute, sublicense, or make derivative works of the Software.

2. Intellectual Property Rights:
   The Software and all intellectual property rights, including but not limited to copyrights, trademarks, trade secrets, and patents, are and will remain the exclusive property of the Licensor. The Licensee agrees not to remove or alter any proprietary notices, trademarks, or copyright information from the Software.

3. Confidentiality:
   The Licensee acknowledges that the Software contains confidential and proprietary information of the Licensor. The Licensee agrees to take reasonable measures to protect the confidentiality of the Software and not disclose or use the Software for any purpose other than as permitted under this Agreement.

4. Disclaimer of Warranty:
   THE SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY, EXPRESS OR IMPLIED. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE LICENSOR DISCLAIMS ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

5. Limitation of Liability:
   TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL THE LICENSOR BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

6. Termination:
   This Agreement is effective until terminated. The Licensor may terminate this Agreement at any time if the Licensee breaches any provision of this Agreement. Upon termination, the Licensee must cease all use of the Software and destroy all copies in its possession or control.

7. Governing Law:
   This Agreement shall be governed by and construed in accordance with the laws of {jurisdiction}, without regard to its conflicts of law principles.

8. Entire Agreement:
   This Agreement constitutes the entire agreement between the parties concerning the subject matter hereof and supersedes all prior and contemporaneous agreements and understandings, whether oral or written.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date of first use of the Software.""","Creative Commons Licenses":"""Creative Commons Attribution 4.0 International (CC BY 4.0)

This is a human-readable summary of (and not a substitute for) the full Creative Commons Attribution 4.0 International license.

You are free to:

  - Share: copy and redistribute the material in any medium or format
  - Adapt: remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

  - Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

No additional restrictions:

  - You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Notices:

  - You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
  - No warranties are given. The license may not give you all the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

Full License:
Commons website: https://creativecommons.org/licenses/by/4.0/legalcode""",
     "BSD License":"""3-Clause BSD License

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
     "Apache Software License":"""Apache License
Version 2.0, January 2004

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   "License" shall mean the terms and conditions for use, reproduction, and distribution as defined by Sections 1 through 9 of this document.

   "Licensor" shall mean the copyright owner or entity authorized by the copyright owner that is granting the License.

   "Legal Entity" shall mean the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.

   "You" (or "Your") shall mean an individual or Legal Entity exercising permissions granted by this License.

   "Source" form shall mean the preferred form for making modifications, including but not limited to software source code, documentation source, and configuration files.

   "Object" form shall mean any form resulting from mechanical transformation or translation of a Source form, including but not limited to compiled object code, generated documentation, and conversions to other media types.

   "Work" shall mean the work of authorship, whether in Source or Object form, made available under the License, as indicated by a copyright notice that is included in or attached to the work (an example is provided in the Appendix below).

   "Derivative Works" shall mean any work, whether in Source or Object form, that is based on (or derived from) the Work and for which the editorial revisions, annotations, elaborations, or other modifications represent, as a whole, an original work of authorship. For the purposes of this License, Derivative Works shall not include works that remain separable from, or merely link (or bind by name) to the interfaces of, the Work and Derivative Works thereof.

   "Contribution" shall mean any work of authorship, including the original version of the Work and any modifications or additions to that Work or Derivative Works thereof, that is intentionally submitted to Licensor for inclusion in the Work by the copyright owner or by an individual or Legal Entity authorized to submit on behalf of the copyright owner. For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to the Licensor or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by the copyright owner as "Not a Contribution."

   "Contributor" shall mean Licensor and any individual or Legal Entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Work.

2. Grant of Copyright License.

   Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work and such Derivative Works in Source or Object form.

3. Grant of Patent License.

   Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Work or a Contribution incorporated within the Work constitutes direct or contributory patent infringement, then any patent licenses granted to You under this License for that Work shall terminate as of the date such litigation is filed.

4. Redistribution.

   You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that You meet the following conditions:

   (a) You must give any other recipients of the Work or Derivative Works a copy of this License; and

   (b) You must cause any modified files to carry prominent notices stating that You changed the files; and

   (c) You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works; and

   (d) If the Work includes a "NOTICE" text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the Derivative Works, in at least one of the following places: within a NOTICE text file distributed as part of the Derivative Works; within the Source form or documentation, if provided along with the Derivative Works; or, within a display generated by the Derivative Works, if and wherever such third-party notices normally appear. The contents of the NOTICE file are for informational purposes only and do not modify the License. You may add Your own attribution notices within Derivative Works that You distribute, alongside or as an addendum to the NOTICE text from the Work, provided that such additional attribution notices cannot be construed as modifying the License.

   You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License.

5. Submission of Contributions.

   Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Work by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions. Notwithstanding the above, nothing herein shall supersede or modify the terms of any separate license agreement you may have executed with Licensor regarding such Contributions.

6. Trademarks.

   This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty.

   Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

8. Limitation of Liability.

   In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability.

   While redistributing the Work or Derivative Works thereof, You may choose to offer, and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS
"""}[license]
def create_setup() -> str:
    """
    Generate the contents of a 'setup.py' file.

    Returns:
        str: The contents of the 'setup.py' file.
    """
##    return f"""from time import time
import setuptools
with open('README.md', "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='{package_name}',
    version='{version}',
    author='{author}',
    author_email='{author_email}',
    description='{description}',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='{url}',
    classifiers={classifiers},
    install_requires={install_requires},
    package_dir={{"": "src"}},  # Fix the package_dir here
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)"""
string = """
Development Status:

Planning
Pre-Alpha
Alpha
Beta
Production/Stable
Mature
Inactive
Intended Audience:

Developers
End Users/Desktop
System Administrators
Science/Research
Education
Financial and Insurance Industry
Healthcare Industry
Information Technology
License:

MIT License
Apache Software License
GNU General Public License (GPL)
BSD License
Mozilla Public License (MPL)
Creative Commons Licenses
Proprietary/Closed Source
Public Domain
Operating System:

OS Independent
Microsoft
MacOS
POSIX (Linux, Unix-like systems)
Android
iOS
Programming Language:

Python
Java
C++
JavaScript
Go
Ruby
PHP
Supported Platforms:

Windows
Linux
macOS
Web (Browser-based)
Mobile (Android, iOS)
Cross-platform
Topic:

Software Developmentf
Internet :: WWW/HTTP
Utilities
Data Science
Machine Learning
Artificial Intelligence
Game Development
Networking
Security
Graphics
Multimedia
Framework:

Django
Flask
React
Angular
TensorFlow
PyTorch
NumPy
SciPy
Keywords:

database
web
API
GUI
automation
testing
visualization
cryptography
natural language processing
robotics
cloud computing
"""
create_folder_bridge["topics_js"] = {}
parsed = string.split('\n')
for each in parsed:
    if ':' in each:
        last = each.split(':')[0]
        topics_js[last]=[]
    else:
        parsed_each = clean_list(each.split('\n'))
        for item in parsed_each:
            item = eatAll(item,['',' ','\n','\t'])
            if len(item)>0:
                topics_js[last].append(item)

def get_all_choice_tags() -> list:
    """
    Get a list of all available choice tags.

    Returns:
        list: A list of choice tags.
    """
    return ["package_name","version","author_name","author","author_email","url","description","long_description"]
def get_readme(location_a: str, location_b: str) -> None:
    """
    Copy the contents of a README file from one location to another.

    Args:
        location_a (str): The source location of the README file.
        location_b (str): The destination location for the README file.

    Returns:
        None
    """
    if os.path.isfile(location_a):
        write_to_file(filepath=os.path.join(location_b,"README.md"),contents=read_from_file(filepath=location_a))
classifiers_layout = []
sections_layout = []
def check_paths() -> None:
    """
    Check and update the status of paths for required files.

    Returns:
        None
    """
    paths={"README.md":{"path":os.path.join(folder,"README.md"),"contents":'',"checked":True},"setup.cfg":{"path":os.path.join(folder,"setup.cfg"),"contents":create_setup_cfg(),"checked":True},"project.toml":{"path":os.path.join(folder,"pyproject.toml"),"contents":create_toml(),"checked":True},"LICENSE":{"path":os.path.join(folder,"LICENSE"),"contents":"","checked":True},
           "src_init":{"path":os.path.join(src_folder,"__init__.py"),"contents":'',"checked":True},"main.py":{"path":os.path.join(module_folder,"main.py"),"contents":get_main_py(),"checked":True},"module_init":{"path":os.path.join(module_folder,"__init__.py"),"contents":'',"checked":True},"setyp.py":{"path":os.path.join(folder,"setup.py"),"contents":create_setup(),"checked":True}}
    for each in paths.keys():
        if os.path.isfile(paths[each]["path"]) == True:
            paths[each]["checked"] = False
        if os.path.isfile(paths[each]["path"]) == False:
            paths[each]["checked"] = True
        create_folder_window_mgr.update_values(window=create_folder_window_mgr.get_last_window_method(),key=each,value=paths[each]["checked"])
def value_function(event: str) -> None:
    """
    Update values and bridge data based on user input events.

    Args:
        event (str): The user input event.

    Returns:
        None
    """
    if event == "default_inputs_submit":
        default_path = create_folder_window_mgr.get_values()["default_inputs"]
        if os.path.isfile(default_path):
            default_js = json.loads(read_from_file(filepath=default_path))
            for each in default_js.keys():
                if each not in ['README.md', 'setup.cfg', 'project.toml', 'LICENSE', 'src_init', 'main.py', 'module_init', 'setyp.py']:
                    try:
                        create_folder_window_mgr.update_values(window=create_folder_window_mgr.get_last_window_method(),key=each,value=default_js[each])
                    except:
                        print('no update on ',each)
    create_folder_bridge["classifiers"] = []
    create_folder_bridge["type_choices"]=create_folder_window_mgr.get_values(window=create_folder_window_mgr.get_last_window_method())
    for each in topics_js.keys():
        if type_choices[each] != '':
            classifiers.append(each+' :: '+type_choices[each])
    create_folder_bridge["classifiers"]=str(classifiers)
    for each in get_all_choice_tags():
        if each in type_choices:
            create_folder_bridge[each]= type_choices[each]
    create_folder_bridge["version"]=''
    for each in ["version_0","version_1","version_2","version_3"]:
        create_folder_bridge["version"]=create_folder_bridge["version"]+type_choices[each]+'.'
    create_folder_bridge["version"] = create_folder_bridge["version"][:-1]
    create_folder_bridge["package_name"] =  type_choices["package_name"]
    create_folder_bridge["parent_folder"] = type_choices["parent_folder"]
    create_folder_bridge["long_description"] = type_choices["long_description"]
    create_folder_bridge["License"] = type_choices["License"]
    if parent_folder != '' and package_name != '' and event != "package_name" and path_checked == False:
        create_folder_bridge["folder"] = os.path.join(parent_folder,package_name)
        mkdirs(folder)
        create_folder_bridge["src_folder"] = os.path.join(folder,"src")
        mkdirs(src_folder)
        create_folder_bridge["module_folder"] = os.path.join(src_folder,package_name)
        mkdirs(module_folder)
        create_folder_bridge["install_requires"] = str(get_installed_versions(scan_folder_for_required_modules(folder)))
        check_paths()
        create_folder_bridge["path_checked"] = True
def write_files() -> None:
    """
    Write contents to files based on user-selected options.

    Returns:
        None
    """
    paths={"README.md":{"path":os.path.join(folder,"README.md"),"contents":'',"checked":False},"setup.cfg":{"path":os.path.join(folder,"setup.cfg"),"contents":create_setup_cfg(),"checked":False},"project.toml":{"path":os.path.join(folder,"pyproject.toml"),"contents":create_toml(),"checked":False},"LICENSE":{"path":os.path.join(folder,"LICENSE"),"contents":"","checked":False},"src_init":{"path":os.path.join(src_folder,"__init__.py"),"contents":'',"checked":False},"main.py":{"path":os.path.join(module_folder,"main.py"),"contents":get_main_py(),"checked":False},"module_init":{"path":os.path.join(module_folder,"__init__.py"),"contents":'',"checked":False},"setyp.py":{"path":os.path.join(folder,"setup.py"),"contents":create_setup(),"checked":False}}
    values = create_folder_window_mgr.get_values(window=create_folder_window_mgr.get_last_window_method())
    for each in paths.keys():
        if values[each] == True and paths[each]["contents"] != None:
            write_to_file(filepath=paths[each]["path"],contents=paths[each]["contents"])

def create_check_marks() -> None:
    """
    Create a layout for checkboxes indicating files to be created.

    Returns:
        None
    """
    create_folder_bridge["check_mark_layout"] = []
    check_list = ['README.md', 'setup.cfg', 'project.toml', 'LICENSE', 'src_init', 'main.py', 'module_init', 'setyp.py']
    for each in check_list:
        check_mark_layout.append([get_gui_fun('Checkbox',args={"text":each,"default":True,"key":each,"enable_events":True})])
def create_inputs(string: str) -> list:
    """
    Create layout elements for user inputs.

    Args:
        string (str): The input string to generate layout elements for.

    Returns:
        list: A list of layout elements for user inputs.
    """
    if string == "long_description":
        return [get_gui_fun('T',{"text":string+':'}),get_gui_fun('Input',args={"default_text":os.getcwd(),"key":string}), get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]#[[get_gui_fun('T',{"text":string+':'})],[get_gui_fun('Input',args={"default":os.getcwd(),"key":string})],[get_gui_fun('FileBrowse', {"initial_folder":os.getcwd()})]]
    elif string == "version":
        return [get_gui_fun('T',{"text":string+':'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_0',"size":(2,1),"enable_events":True}),get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_1',"size":(2,1),"enable_events":True}),get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_2',"size":(2,1),"enable_events":True}),get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_3',"size":(2,1),"enable_events":True})]
    elif string == "description":
        return [get_gui_fun('T',{"text":string+':'}),get_gui_fun('Multiline',args={"key":string,"size":(20,10),"enable_events":True})]
    return [get_gui_fun('T',{"text":string+':'}),get_gui_fun('Input',args={"key":string,"size":(20,1),"enable_events":True})]

def create_dropdown(string: str, ls: list) -> list:
    """
    Create a dropdown layout for user choices.

    Args:
        string (str): The dropdown label.
        ls (list): The list of choices for the dropdown.

    Returns:
        list: A list of layout elements for a dropdown.
    """
    return [get_gui_fun('T',{"text":string+':'}),get_gui_fun('Combo',args={"values":ls,"key":string,"default_value":ls[0],"enable_events":True})]
def create_module_folder() -> str:
    """
    Create a new module folder and generate necessary files based on user input.

    Returns:
        str: The path of the created module folder.
    """
    for each in topics_js.keys():
        classifiers_layout.append(create_dropdown(each,topics_js[each]))
    classifiers_layout = [get_gui_fun("Frame",args={"title":"classifiers","layout":classifiers_layout})]
    for each in get_all_choice_tags():
        sections_layout.append(create_inputs(each))
    create_check_marks()
    create_folder_bridge["path_checked"] = False
    sections_layout = [get_gui_fun("Frame",args={"title":"classifiers","layout":sections_layout})]
    default_inputs_layout = [get_gui_fun("Frame",args={"title":"choose default inputs","layout":[[sg.Button("default_inputs_submit"),get_gui_fun('Input',args={"default_text":os.path.join(os.getcwd(),"default_inputs.json"),"key":"default_inputs"}), get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]]})]
    parent_folder_layout = [get_gui_fun("Frame",args={"title":"Parent Folder","layout":[[get_gui_fun('Input',args={"default_text":os.getcwd(),"key":"parent_folder"}), get_gui_fun('FolderBrowse', {"initial_folder": os.getcwd()})]]})]
    check_mark_layout = [get_gui_fun("Frame",args={"title":"Files To Create","layout":ensure_nested_list(check_mark_layout)})]
    layout = [[default_inputs_layout],[parent_folder_layout],[sections_layout],[classifiers_layout],[check_mark_layout]]
    window = create_folder_window_mgr.get_new_window(args={"title":'setup_window','layout':ensure_nested_list([layout,[sg.Button("Submit")]])},event_function="value_function",exit_events=["Submit"])
    create_folder_window_mgr.while_basic(window)
    write_files()
    write_to_file(filepath=os.path.join(parent_folder,"default_inputs.json"),contents=json.dumps(type_choices))
    return create_folder_bridge["module_folder"]
