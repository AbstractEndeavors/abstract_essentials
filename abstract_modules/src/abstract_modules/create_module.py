from abstract_utilities.time_utils import get_current_year
from abstract_utilities.string_clean import eatAll
from abstract_utilities.class_utils import get_fun
from abstract_utilities.path_utils import mkdirs,get_base_name,get_directory
from abstract_utilities.read_write_utils import write_to_file,read_from_file
from .module_utils import get_installed_versions,scan_folder_for_required_modules
from .upload_utils import upload_main
from abstract_gui import *
from datetime import datetime
import os
import json
create_folder_window_mgr,folder_bridge,create_folder_script = create_window_manager(script_name='create_folder_script',global_var=globals())
folder_bridge=folder_bridge.return_global_variables(script_name=create_folder_script)
folder_bridge["MODULE_FOLDER"]=None
folder_bridge["MODULE_NAV_HISTORY"] = []
folder_bridge["folder"] = os.getcwd()
import setuptools
import os
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
    now = datetime.now()
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
def licenses(license:str="MIT",args:dict={"author_name":"name","year":str(get_current_year()),"company_name":'["Company Name"]',"jurisdiction":"[Your jurisdiction]","software_name":'("the Software")',"licensee":'("the Licensee")',"licensor":'("the Licensor")'}):
    author_name, year, company_name, jurisdiction, software_name, licensee, licensor = args.values()
    if license == '':
        license="MIT"
    """
    Generate a license text with specified parameters.

    Args:
        license (str): The chosen license type.
        args (dict): A dictionary containing parameter values for the license text.

    Returns:
        str: The generated license text with formatted parameters.
    """
    return {"Public Domain":"""Public Domain Dedication========================

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
def create_setup(package_name:str="package",
                 version:str='0.0.0.1',
                 author:str="author",
                 author_email:str="author_email",
                 description:str="description",
                 url:str="url",
                 classifiers:list=[],
                 install_requires:list=[]) -> str:
    """
    Generate the contents of a 'setup.py' file.

    Returns:
        str: The contents of the 'setup.py' file.
    """
    return f"""from time import time
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
    setup_requires=['wheel'],
)"""
def get_main_py(package_name:str="package",
                 version:str='0.0.0.1',
                 author:str="author",
                 author_email:str="author_email",
                 description:str="description",
                 url:str="url",
                 classifiers:list=[],
                 install_requires:list=[]) -> str:
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

def create_setup_cfg(*args) -> str:
    """
    Create the contents of a 'setup.cfg' file.

    Returns:
        str: The contents of the 'setup.cfg' file.
    """
    return f'''[bdist_wheel]
tag_build = dev
tag_date = {get_tag_date()}'''
def create_toml(*args) -> str:
    """
    Create the contents of a 'pyproject.toml' file.

    Returns:
        str: The contents of the 'pyproject.toml' file.
    """
    return f'''[build-system]
    requires = ["{get_installed_versions(['setuptools'])}"]
    build-backend = "setuptools.build_meta"'''
def make_columns(columns,layout,current_row,obj,num,max_num,last_bool:bool=False):
    num +=1
    current_row.append(obj)
    if (num) % columns == 0:  # +1 because index starts from 0
        layout.append(current_row)
        current_row = []

    # If there are remaining checkboxes that didn't make a full row of 3, add them
    if last_bool or num == max_num:
        layout.append(current_row)
    return num,current_row,layout
def return_largest_size(js,var):
    highest=0
    for each in js[var]:
        if len(each)>highest:
            highest=len(each)
    return highest
def new_layout(string:str,i):
    lay = [get_gui_fun('Combo',args={"values":get_dev_status_js()[string],"value":get_dev_status_js()[string][0],"size":(return_largest_size(get_dev_status_js(),string),1),"key":"-DEV_STATUS_"+string+str(i)+'-',"enable_events":True})]
    if string == "Programming Language":
        lay.append(get_gui_fun('Input',args={"default_text":"","key":"-VERSION_PY"+str(i)+"-","size":(5,1)}))
    return [lay]

def capture_setup(**kwargs):
    global setup_data
    setup_data = kwargs

def parse_setup(file_path: str = None):
    os.chdir(get_directory(file_path))
    original_setup = setuptools.setup
    setuptools.setup = capture_setup

    with open('setup.py', 'r') as f:
        setup_script = f.read()

    setup_data = {}
    exec(setup_script, {'setuptools': setuptools})

    keys_to_extract = ['package_name', 'version', 'author', 'author_email', 'description', 'url', 'classifiers']

    for key in keys_to_extract:
        value = setup_data.get(key)
        if value:
            print(f"{key}: {value}")
    return setup_data

def capture_setup_(**kwargs):
        return kwargs

def create_classifiers():
    values = get_values()
    total_type_dev_ls=[]
    for each in values.keys():
        if "-DEV_STATUS_" in each:
            type_num=''
            if values[each] != "":
                type_dev_ls = []
                type_dev = each[len("-DEV_STATUS_"):-1]
                if type_dev[-1] in '0,1,2,3,4,5,6,7,8,9'.split(','):
                    type_num = type_dev[-1]
                    type_dev=type_dev[:-1]
                type_dev_ls.append(type_dev)
                type_dev_ls.append(values[each])
                if type_dev == "Programming Language":
                    type_dev_ls.append(values["-VERSION_PY_"+type_dev+type_num+'-'])
                total_type_dev_ls.append(type_dev_ls)
    classifiers_list = []
    for each in total_type_dev_ls:
        new_item = ''
        for i,item in enumerate(each):
            new_item+=item
            if i != len(each)-1:
                new_item +=' :: '
        classifiers_list.append(new_item)
    return classifiers_list
def parse_setup(file_path:str=None):


    lines = read_from_file(file_path).split('\n')
    for line_num,each in enumerate(lines):
        line = eatAll(each,['',' ','\n','\t'])
        split_line = line.split('=')
        if split_line[0] in ['package_name','version','author','author_email','description','url','classifiers']:
            if split_line[0] in ['version','classifiers']:
                if split_line[0] == 'version':
                    value = line[len(split_line[0])+1:]
                    if ',' == value[-1]:
                        value = value[:-1]
                    for i,vers in enumerate(value.split('.')):
                        update_values(split_line[0]+'_'+str(i),{"value":eatAll(vers,['"',"'",'',' ','\n','\t',',','[',']'])})
                elif split_line[0] in 'classifiers':
                    keys = list(get_dev_status_js().keys())
                    classifiers=[line[len(split_line[0])+1:]]
                    for each in lines[line_num+1:]:
                        if '=' not in each:
                            classifiers.append(eatAll(each,['"',"'",'',' ','\n','\t',',','[',']']))
                        else:
                            break
                    have = []
                    for classifier in classifiers:
                         spl = classifier.split(' :: ')
                         key = eatAll(spl[0],['"',"'",'',' ','\n','\t',',','[',']'])
                         if key in keys:
                             replace_key = "-DEV_STATUS_"+key+'-'
                             version = "-VERSION_PY_"+key+'-'
                             if key in have:

                                 count = -1
                                 for i in range(len(have)):
                                     if have[i] == key:
                                         count +=1
                                 if count != 0:      
                                     version ="-VERSION_PY_"+key+str(count)+'-'
                                     replace_key = "-DEV_STATUS_"+key+str(count)+'-'
                                 if replace_key not in get_values():
                                     folder_bridge["window"].extend_layout(folder_bridge["window"]["-COLUMN"+"_"+key+"-"], new_layout(key,count))
                             have.append(key)
                             update_values(replace_key ,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']'])})
                             if "Programming Language" == key:
                                 update_values(replace_key ,{"value":eatAll(spl[1],['"',"'",'',' ','\n','\t',',','[',']'])})
                                 update_values(version,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']'])})
                             if  "Development Status"== key:
                                update_values(replace_key ,{"value":eatAll(spl[-1],['"',"'",'',' ','\n','\t',',','[',']']).split('- ')[-1]})

            else:
                value = line[len(split_line[0])+1:]
                if ',' == value[-1]:
                    value = value[:-1]

                update_values(split_line[0] ,{"value":eatAll(value,['"',"'",'',' ','\n','\t',',','[',']'])})

def list_all_directories(root_folder):
    """
    Recursively list all directories starting from root_folder.
    """
    directories = []
    if os.path.isdir(root_folder):
        directories.append(root_folder)
        for child in os.listdir(root_folder):
            child_path = os.path.join(root_folder, child)
            directories.extend(list_all_directories(child_path))
    return directories
def generate_directory_map(root_folder):
    """
    Recursively generate a dictionary mapping of folder and its content.
    """
    directory_map = {}
    if os.path.isdir(root_folder):
        directory_map[root_folder] = [os.path.join(root_folder, child) for child in os.listdir(root_folder)]
        for child in directory_map[root_folder]:
            directory_map.update(generate_directory_map(child))
    return directory_map
def get_values():
    try:
        values = create_folder_window_mgr.get_values(window=folder_bridge["window"])
    except:
        values={}
    return values
def update_values(key,args):
    if key != None:
        create_folder_window_mgr.update_values(window=folder_bridge["window"],key=key,args=args)
def get_all_choice_tags() -> list:
    """
    Get a list of all available choice tags.

    Returns:
        list: A list of choice tags.
    """
    return ["package_name","version","author_name","author","author_email","url","description","long_description"]
def get_dev_status_js():
    return {
        "Development Status":["Planning","Pre-Alpha","Alpha","Beta","Production/Stable","Mature","Inactive"],
        "Intended Audience":["Developers","End Users/Desktop","System Administrators","Science/Research","Education","Financial and Insurance Industry","Healthcare Industry","Information Technology"],
        "License":["MIT License","Apache Software License","GNU General Public License (GPL)","BSD License","Mozilla Public License (MPL)","Creative Commons Licenses","Proprietary/Closed Source","Public Domain"],
        "Operating System":["OS Independent","Microsoft","MacOS","POSIX (Linux, Unix-like systems)","Android","iOS"],
        "Programming Language":["Python","Java","C++","JavaScript","Go","Ruby","PHP"],
        "Supported Platforms":["Windows","Linux","macOS","Web (Browser-based)","Mobile (Android, iOS)","Cross-platform"],
        "Topic":["Software Developmentf","Internet :: WWW/HTTP","Utilities","Data Science","Machine Learning","Artificial Intelligence","Game Development","Networking","Security","Graphics","Multimedia"],
        "Framework":["Django","Flask","React","Angular","TensorFlow","PyTorch","NumPy","SciPy"],
        "Keywords":["database","web","API","GUI","automation","testing","visualization","cryptography","natural language processing","robotics","cloud computing"]
        }
def create_dev_status():
    layout = []
    current_row=[]
    num = 0
    dev_status_json = get_dev_status_js()
    for each in dev_status_json.keys():
        dev_status_value = dev_status_json[each]

        if each=="Programming Language":
            lay = [get_gui_fun("Combo",args={"values":dev_status_value,"value":dev_status_value[0],"size":(9,1),"key":"-DEV_STATUS_"+each+'-',"enable_events":True})]
            lay.append(get_gui_fun('Input',args={"default_text":"version","key":"-VERSION_PY_"+each+"-","size":(4,1)}))
        else:
            lay = [get_gui_fun("Combo",args={"values":dev_status_value,"value":dev_status_value[0],"size":(15,1),"key":"-DEV_STATUS_"+each+'-',"enable_events":True})]
        lay.append(get_gui_fun("Button",args={"button_text":"+","key":"-DEV_STATUS_"+each+"_BUTTON-","enable_events":True}))
        num,current_row,layout=make_columns(columns=3,
                                            layout=layout,current_row=current_row,obj=get_gui_fun("Frame",args={"title":each,"layout":ensure_nested_list(lay),"key":"-COLUMN"+"_"+each+"-"}),num=num,max_num=len(dev_status_json.keys()))
    return  get_gui_fun("Frame",args={"title":"Choose Dev Status","layout":ensure_nested_list(layout),"key":"-COLUMN-"
                                      ,"scrollable":True,"expand_x":False,"auto_scroll":True,"min_size":(200,200),**expandable()})
def create_toml(*args) -> str:
    """
    Create the contents of a 'pyproject.toml' file.

    Returns:
        str: The contents of the 'pyproject.toml' file.
    """
    return f'''[build-system]
    requires = ["{get_installed_versions(['setuptools'])}"]
    build-backend = "setuptools.build_meta"'''
def create_check_marks() -> None:
    """
    Create a layout for checkboxes indicating files to be created.

    Returns:
        None
    """
    check_mark_layout = []
    current_row = []
    num = 0
    file_associations=get_file_associations()
    check_list = file_associations.keys()
    for i, each in enumerate(check_list):
        check = get_gui_fun('Checkbox', args={"text": file_associations[each]["file"], "default": True, "key": each[:-1]+'_CHECK-', "enable_events": True})
        num,current_row,layout=make_columns(columns=2,
                                            layout=check_mark_layout,current_row=current_row,obj=check,num=num,max_num=len(check_list))
    layout[-1].append(sg.Button("Create Files"))
    layout[-1].append(sg.Button("Create Module",key="-CREATE_FOLDER-",enable_events=True))

    return get_gui_fun("Frame",args={"title":"File Checklist","layout":ensure_nested_list(layout)})
def create_inputs(string: str) -> list:
    """
    Create layout elements for user inputs.

    Args:
        string (str): The input string to generate layout elements for.

    Returns:
        list: A list of layout elements for user inputs.
    """
    if string == "long_description":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Input',args={"default_text":os.getcwd(),"key":string}),
                get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]#[[get_gui_fun('T',{"text":string+':'})],[get_gui_fun('Input',args={"default":os.getcwd(),"key":string})],[get_gui_fun('FileBrowse', {"initial_folder":os.getcwd()})]]
    elif string == "version":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Input',args={"default_text":"0","key":string+'_0',"size":(2,1),"enable_events":True}),get_gui_fun('T',{"text":'.'}),
                get_gui_fun('Input',args={"default_text":"0","key":string+'_1',"size":(2,1),"enable_events":True}),
                get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_2',"size":(2,1),"enable_events":True}),
                get_gui_fun('T',{"text":'.'}),get_gui_fun('Input',args={"default_text":"0","key":string+'_3',"size":(2,1),"enable_events":True})]
    elif string == "description":
        return [get_gui_fun('T',{"text":string+':'}),
                get_gui_fun('Multiline',args={"key":string,"size":(None,None),"enable_events":True,**expandable()})]
    return [get_gui_fun('T',{"text":string+':'}),
            get_gui_fun('Input',args={"key":string,"size":(20,1),"enable_events":True})]
def create_choice_tag_layout():
    choice_tag_layout=[]
    choice_tags = get_all_choice_tags()
    for each in choice_tags:
        if each not in ["description","long_description"]:
            choice_tag_layout.append(create_inputs(string=each))
    return get_gui_fun("Frame",args={"title":"Choice Tags","layout":ensure_nested_list(choice_tag_layout)})
def get_descriptions_layout():
    description_layout=[]
    description_list = ["description","long_description"]
    for each in description_list:
        description_layout.append(create_inputs(string=each))
    return get_gui_fun("Frame",args={"title":"Descriptions","layout":ensure_nested_list(description_layout),**expandable()})
def get_module_folder_browser(initial_folder:str="/home/john-putkey/Documents/modules/abstract_audio"):

    return [
             get_gui_fun("Frame",args={"title":"Choose Module Directory","layout":ensure_nested_list([
                 get_gui_fun('Input',args={"default_text":initial_folder,"disabled":False,"key":"-MODULE_PERMENANT_PATH-","enable_events":True}),
                 get_gui_fun('Input',args={"default_text":initial_folder,"key":"-MODULE_FOLDER_PATH-","enable_events":True}),
                                                                                                     get_gui_fun('FolderBrowse', {"initial_folder": initial_folder,"key":"-MODULE_FOLDER_BROWSER-","enable_events":True}),
                                                                                                     get_gui_fun("Checkbox",args={"text":"choose folder","default":False,"key":"-LOCK_CHECKBOX-","enable_events":True})])})]



def create_init():
    return ''
def get_file_associations():
    values = get_values()
    if 'package_name' not in values:
        values["package_name"]=''
    return {'-README-':{"directory":"","file":"README.md","function":"get_readme"},
                       '-SETUP_CFG-':{"directory":"","file":"setup.cfg","function":"create_setup_cfg"},
                       '-PROJECT_TOML-':{"directory":"","file":"project.toml","function":"create_toml"},
                       '-LICENSE-':{"directory":"","file":"LICENSE.txt","function":"licenses"},
                       '-SETUP_PY-':{"directory":"","file":"setup.py","function":"create_setup"},
                        "-SRC_INIT-":{"directory":f"src/","file":"__init__.py","function":"create_init"},
                       '-MODULE_INIT-':{"directory":f"src/{values['package_name']}","file":"__init__.py","function":"create_init"},
                       '-MAIN_PY-':{"directory":f"src/{values['package_name']}","file":"main.py","function":"get_main_py"},
                       }
def get_all_choice_tags() -> list:
    """
    Get a list of all available choice tags.

    Returns:
        list: A list of choice tags.
    """
    return ["package_name","version","author_name","author","author_email","url","description","long_description"]
def return_opposite_bool(bool_it):
    if isinstance(bool_it,bool):
        if bool_it:
            return False
        return True
def check_all_files(directory:str):
    name = directory.split('/')[-1]
    update_values('package_name',{"value":name})
    file_associations = get_file_associations()
    for each in file_associations.keys():
       file_path = os.path.join(directory,file_associations[each]["directory"],file_associations[each]["file"])
       file_exists = os.path.exists(file_path)
       
       update_values(each[:-1]+'_CHECK-',{"value":return_opposite_bool(file_exists)})
       if file_exists and file_associations[each]["file"] == "setup.py":
           parse_setup(file_path)
def get_readme(readme_path:str=None):
    contents = ''
    if os.path.isfile(readme_path):
        contents = read_from_file(readme_path)
    write_to_file(filepath=os.path.join(get_values()["-MODULE_PERMENANT_PATH-"],"README.md"),contents=contents)
    return None
def create_module_folder() -> str:
    """
    Create a new module folder and generate necessary files based on user input.

    Returns:
        str: The path of the created module folder.
    """
    for each in folder_bridge["topics_js"].keys():
        folder_bridge["classifiers_layout"].append(create_dropdown(each,folder_bridge["topics_js"][each]))
    folder_bridge["classifiers_layout"] = [get_gui_fun("Frame",args={"title":"classifiers","layout":folder_bridge["classifiers_layout"]})]
    for each in get_all_choice_tags():
        folder_bridge["sections_layout"].append(create_inputs(each))
    create_check_marks()
    folder_bridge["path_checked"] = False
    folder_bridge["sections_layout"] = [get_gui_fun("Frame",args={"title":"classifiers","layout":folder_bridge["sections_layout"]})]
    default_inputs_layout = [get_gui_fun("Frame",args={"title":"choose default inputs","layout":[[sg.Button("default_inputs_submit"),get_gui_fun('Input',args={"default_text":os.path.join(os.getcwd(),"default_inputs.json"),"key":"default_inputs"}), get_gui_fun('FileBrowse', {"initial_folder": os.getcwd()})]]})]
    parent_folder_layout = [get_gui_fun("Frame",args={"title":"Parent Folder","layout":[[get_gui_fun('Input',args={"default_text":os.getcwd(),"key":"parent_folder"}), get_gui_fun('FolderBrowse', {"initial_folder": os.getcwd()})]]})]
    folder_bridge["check_mark_layout"] = [get_gui_fun("Frame",args={"title":"Files To Create","layout":ensure_nested_list(folder_bridge["check_mark_layout"])})]
    folder_bridge["license_layout"] = [get_gui_fun("Frame",args={"title":"license","layout":ensure_nested_list([get_gui_fun("Combo",args={"values":list(get_license_json().keys()),"default_value":list(get_license_json().keys())[0],"enable_events":True,"key":"-LICENSE-"})])})]
    layout = [[default_inputs_layout],[parent_folder_layout],[folder_bridge["sections_layout"],folder_bridge["license_layout"]],[folder_bridge["classifiers_layout"]],[folder_bridge["check_mark_layout"]]]
    window = create_folder_window_mgr.get_new_window(args={"title":'setup_window','layout':ensure_nested_list([layout,[sg.Button("Submit")]])},event_function="value_function",exit_events=["Submit"])
    create_folder_window_mgr.while_basic(window)
    write_files()
    write_to_file(filepath=os.path.join(parent_folder,"default_inputs.json"),contents=json.dumps(folder_bridge["type_choices"]))
    return folder_bridge["module_folder"]
def create_new_module(event:str=None):
    if create_folder_window_mgr.get_event() == 'Create':
        values=create_folder_window_mgr.get_values(window=create_folder_window_mgr.get_last_window_method())
        if values['-NEW_FOLDER_NAME-'] and values['-PARENT_DIR-']:
            folder_path = os.path.join(values['-PARENT_DIR-'], values['-NEW_FOLDER_NAME-'])
            os.makedirs(folder_path, exist_ok=True)
            return folder_path
def while_module(event):
    values = get_values()
    file_associations = get_file_associations()
    if event == "-UPLOAD_MODULE-":
        upload_main(project_dir=values["-MODULE_PERMENANT_PATH-"])
    if event == "Create Files":
        args = {"readme_path":values["long_description"],
                            'README.md':values["long_description"],
                            "license":values["-DEV_STATUS_License-"],
                            "package_name":values["package_name"],
                            "version":values["version_0"]+'.'+values["version_1"]+'.'+values["version_2"]+'.'+values["version_3"],
                            "author":values["author"],
                            "author_email":values["author_email"],
                            "description":values["description"],
                            "url":values["url"],
                            "classifiers":create_classifiers(),
                            "install_requires":get_installed_versions(scan_folder_for_required_modules(values["-MODULE_PERMENANT_PATH-"],"src"))[0]}
        for each in file_associations.keys():
            if "function" in file_associations[each]:
                if values[each[:-1]+'_CHECK-'] == True:
                    contents = get_fun({"args":args,"global":globals(),"name":file_associations[each]["function"]})
                    file_path = os.path.join(values["-MODULE_PERMENANT_PATH-"],file_associations[each]["directory"],file_associations[each]["file"])
                    if contents != None:
                        write_to_file(filepath=file_path,contents=contents)


    if "-DEV_STATUS_" in event and event[-len("_BUTTON-"):] == "_BUTTON-":
        i=0
        while event[:-len("_BUTTON-")]+str(i)+'-' in values:
            i+=1
        key = event[len("-DEV_STATUS_"):-len("_BUTTON-")]
        folder_bridge["window"].extend_layout(folder_bridge["window"]["-COLUMN"+"_"+key+"-"],new_layout(key,i))
    folder_contents={"parent":['README.md', 'setup.cfg', 'project.toml', 'LICENSE','setup.py'] , "src":['src_init'],"module":['main.py','module_init']}
    if event == "-CREATE_FOLDER-":

        layout=[[get_gui_fun("Text",args={"text":'Enter the new folder name:'})],
        [get_gui_fun("Input",args={"key":'-NEW_FOLDER_NAME-'})],
        [get_gui_fun("Text",args={"text":'Select Parent Directory:'})],
        [get_gui_fun("Input",args={"default_text":get_values()["-MODULE_PERMENANT_PATH-"],"key":"-PARENT_DIR-", "disabled":True}), get_gui_fun("FolderBrowse",args={"initial_folder":get_values()["-MODULE_PERMENANT_PATH-"]})],
        [create_row_of_buttons('Create','Cancel')]]
        new_folder_name=create_folder_window_mgr.while_basic(create_folder_window_mgr.get_new_window(args={"layout":layout,"title":"please choose a folder name and path","event_function":"create_new_module","exit_events":["Cancel","Create"]}))
        new_folder_path = create_new_module(new_folder_name)
        if new_folder_path:
            os.makedirs(new_folder_path, exist_ok=True)
            update_values("-MODULE_FOLDER_PATH-", {"value":new_folder_path})

            update_values("-DIRECTORY_LIST-", {"values": os.listdir(new_folder_path)})
    elif event == "-DIRECTORY_LIST-":
        chosen_path = None
        if len(values["-DIRECTORY_LIST-"]) != 0:
            chosen_folder = values["-DIRECTORY_LIST-"][0]  # This retrieves the selected folder from the listbox
            if values["-MODULE_FOLDER_PATH-"] != None:
                chosen_path = os.path.join(values["-MODULE_FOLDER_PATH-"], chosen_folder)
            if chosen_path != None:
                if os.path.isdir(chosen_path):  # This checks if the selected item is a directory
                    update_values("-MODULE_FOLDER_PATH-", {"value":chosen_path})
                    update_values("-MODULE_PERMENANT_PATH-", {"value":chosen_path})
                    folder_bridge["MODULE_FOLDER"]=chosen_path
                    update_values("-DIRECTORY_LIST-", {"values": os.listdir(chosen_path)})
                    if not values["-LOCK_CHECKBOX-"]:
                        update_values("-MODULE_PERMENANT_PATH-",{"value":chosen_path})
            else:
                create_folder_window_mgr.while_basic(create_folder_window_mgr.get_new_window(title="warning",layout=[[get_gui_fun('T', {"text": f"{chosen_folder} is not a directory."})],create_row_of_buttons("OK")],exit_events=["OK"]))
    if event == "-LOCK_CHECKBOX-":
        if not values["-LOCK_CHECKBOX-"]:
            #folder_bridge["window"]["-MODULE_PERMENANT_PATH-"].update(disabled=True)
            update_values("-MODULE_PERMENANT_PATH-",{"disabled":False})
            folder_bridge["MODULE_FOLDER"] = None
        elif values["-LOCK_CHECKBOX-"]:
            update_values("-MODULE_PERMENANT_PATH-",{"value":values["-MODULE_FOLDER_PATH-"]})
            update_values("-MODULE_PERMENANT_PATH-",{"disabled":True})
            folder_bridge["MODULE_FOLDER"]=values["-MODULE_PERMENANT_PATH-"]
            check_all_files(folder_bridge["MODULE_FOLDER"])


    if event in ["-MODULE_FOLDER_PATH-","-MODULE_FOLDER_BROWSER-"]:
        if os.path.exists(values["-MODULE_FOLDER_PATH-"]):
            update_values("-DIRECTORY_LIST-", {"values": os.listdir(values["-MODULE_FOLDER_PATH-"])})
            folder = values["-MODULE_FOLDER_PATH-"]  # fetch the folder path
            if folder:
                update_values("-MODULE_FOLDER_PATH-", {"value":folder})  # update the input text with the folder path

                if not values["-LOCK_CHECKBOX-"]:
                    update_values("-MODULE_PERMENANT_PATH-", {"value":folder})  # if not locked, update the permanent directory input text too
    elif event == '<-':
        current_folder = values["-MODULE_FOLDER_PATH-"]
        parent_folder = os.path.dirname(current_folder) if current_folder else None
        if folder_bridge["MODULE_FOLDER"] != None:
            if parent_folder in list_all_directories(folder_bridge["MODULE_FOLDER"]):
                update_values("-MODULE_FOLDER_PATH-", {"value": parent_folder})
                update_values("-DIRECTORY_LIST-", {"values": os.listdir(parent_folder)})

        elif parent_folder and os.path.exists(parent_folder):
            update_values("-MODULE_FOLDER_PATH-", {"value": parent_folder})
            update_values("-DIRECTORY_LIST-", {"values": os.listdir(parent_folder)})

            # Add current folder to history
            folder_bridge["MODULE_NAV_HISTORY"].append(current_folder)

    elif event == '->':
        if folder_bridge["MODULE_NAV_HISTORY"]:
                next_folder = folder_bridge["MODULE_NAV_HISTORY"].pop()
                if folder_bridge["MODULE_FOLDER"] != None:
                    all_directories = list_all_directories(folder_bridge["MODULE_FOLDER"])
                    all_directories.append(folder_bridge["MODULE_FOLDER"])
                    if next_folder in all_directories:
                        update_values("-MODULE_FOLDER_PATH-", {"value": next_folder})
                        update_values("-DIRECTORY_LIST-", {"values": os.listdir(next_folder)})


                elif os.path.exists(next_folder):
                    #folder_bridge["MODULE_FOLDER"] = next_folder
                    update_values("-MODULE_FOLDER_PATH-", {"value": next_folder})
                    update_values("-DIRECTORY_LIST-", {"values": os.listdir(next_folder)})
def get_layout():
    listbox= [[]]

    folder_bridge["window"] = create_folder_window_mgr.get_new_window("create module",
                                                     args={'layout':[[
                                                         get_gui_fun("Listbox", args={"values": os.listdir(os.getcwd()), "size": (20, 20), "key": "-DIRECTORY_LIST-", "bind_return_key": True, "enable_events": True}),
                                                         create_row_of_buttons('<-','->'),
                                                         create_check_marks(),
                                                         get_descriptions_layout(),get_module_folder_browser()],
                                                         [create_dev_status(),[]]],"event_function":"while_module",**expandable()})
    create_folder_window_mgr.while_basic(folder_bridge["window"])
def run_module_consol():
    listbox= get_gui_fun("Listbox", args={"values": os.listdir(os.getcwd()), "size": (20, 20), "key": "-DIRECTORY_LIST-", "bind_return_key": True, "enable_events": True})
    buttons = create_row_of_buttons('<-','->')
    listbox_column = sg.Column([[listbox],buttons])
    check_marks_column = sg.Column([[create_check_marks()],[create_choice_tag_layout()]])
    status_column = sg.Column([[create_check_marks(),create_choice_tag_layout()],[create_dev_status()]])
    top_frame =get_gui_fun("Frame",args={"title":"","layout":[[listbox_column,status_column],get_module_folder_browser(),[get_gui_fun("Button",args={"button_text":"dev_status","enable_events":True,"key":"-UPLOAD_MODULE-"})]]})
    folder_bridge["window"] = create_folder_window_mgr.get_new_window("create module",
                                                     args={'layout':[[get_descriptions_layout(),[top_frame]
                                                        ]],"event_function":"while_module","min_size":(500,500),"max_size":(1000,1000),"resizable":True, "pad":(0,0)})
    create_folder_window_mgr.while_basic(folder_bridge["window"])
