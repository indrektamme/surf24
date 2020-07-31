from surf24 import db
from flask import Blueprint
from surf24.models import Category
from surf24.categories.forms import CategoryForm

categories = Blueprint('categories', __name__)

def makeCategoryForm(choice1, choice2, choice3, size=0, brand="", form = None):
    print(f"size on {size}")
    if size == None: size = 0
    if form == None: form = CategoryForm()
    form.category1.choices = createCategoryChoices(0)
    form.category2.choices = createCategoryChoices(choice1)
    if ifCategoryHasParent(choice2, choice1): form.category3.choices = createCategoryChoices(choice2)

    if float(size) > 0: form.size.data = size
    if brand: form.brand.data = brand
    form.category1.default = choice1
    form.category2.default = choice2
    form.category3.default = choice3

    return form

def createCategoryChoices(parent):
    choices = []
    if parent == None: parent = 1000
    choices1 = Category.query.filter_by(parent=parent).all()
    for element in choices1:
        sequence = (element.id, element.name)
        choices.append(sequence)
    return choices

def ifCategoryHasParent(categoryId, parentId):
    if categoryId:
        category = Category.query.get(categoryId)
        if category != None:
            if category.parent == parentId:
                return True
    return False
