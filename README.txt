Introduction
============

SimpleLayout provides an intuitive way of adding and arranging the different 
elements of a page such as paragraphs, images, files and links using 
drag-and-drop functionality. 
These elements are implemented as addable and easily arrangeable "blocks". 
Because of the restricted dimensions of text, images and other content elements, 
the general result is content with a uniform look and feel throughout the site. 


How to use SimpleLayout
=======================

Check out our new video section on plone.org:
http://plone.org/products/simplelayout.base/documentation

1.) Add a new Page from the "Add new" dropdown.

In this page one can now add the following page elements:

- File
- Image
- Link
- Page
- Paragraph

2.) Add a new Paragraph from the "Add new" dropdown:

- Provide a title for the new paragraph (not required) and check "Show Title" 
  to determine whether the paragraph title will appear in the page's body text.
- Provide body text for the paragraph.(Of course one could use this first 
  paragraph to provide the text for the whole page, but that would defeat the 
  purpose of having easily arrangeable "blocks" of text and other page elements)

Image tab:

- Browse for an image and provide a caption and alternative text.
- Determine whether the image is "clickable", i.e. whether the image source can 
  be opened in a new tab. If collective.greybox is installed, it will use 
  greybox to show the image. 

Settings tab:

- Provide keywords/tags for categorization purposes.
- Specify "Related Items": If the "teaser" box is checked, related items of this 
  paragraph will be displayed underneath the paragraph.
- Provide "Creators" (Persons responsible for creating the content of this item).
- Allow comments.
- Determine whether this paragraph should be included in the site navigation 
  (by default it is not included).

When saving the paragraph, one is redirected to the edit tab of the parent page.
Here one is presented with the option of editing the page as a whole, or editing 
one of the sub-elements of the page.
The layout of the recently added paragraph can be further manipulated using the 
layout icons in the top panel of the that paragraph.  
The paragraph can also easily be deleted from here, or its order in the page 
changed using the "ordering" arrow icons in its top panel (will be removed, 
you should use the drag'n'drop funtionality).

3.) Add an Image to the page from the "Add new" dropdown:

- Browse for an image and provide alternative text. The Title is used as the 
  image caption.

4.) Add a File to the page from the "Add new" dropdown:

- Browse for and add a file (for example a pdf). The file download link will be 
  displayed in the page content.

5.) Add a Link to the page from the "Add new" dropdown:

- Specify an external link, which will be displayed in the page.

6.) Add another page:
The parent page acts as a container in which sub pages can be added.
These will appear in the site navigation.


Page Layout:
------------

To add layout functionality to the page as a whole, go to 
"Site Setup" => "Simplelayout Configuration", and check "Show Design".
A "Design" dropdown will be added to your SimpleLayout pages, from which you can 
choose one of 3 possible layouts: Normal, Two Columns, Two Columns One on Top
Here one can also determine the dimensions of the layout columns by providing pixel 
values in the other 2 "configuration" tabs.

Go to the edit tab of your SimpleLayout page and choose another layout from the 
"Design" dropdown.

In "Two Columns" designs it's possible to align the blocks like a table. 
Use the "align to grid" link in the top panel of the page. 

Drag and drop functionality:
----------------------------
Drag the existing content blocks into the other areas of the newly created layout, 
by clicking on the top panel and dragging the block to the desired position. 


Support of following products is allready included
--------------------------------------------------

* collective.greybox
* Products.PloneFlashUpload 
  tested with http://svn.plone.org/svn/collective/PloneFlashUpload/branches/dunny-flash-10-support-via-swfupload-2.2


Simplelayout provides the following features:
=============================================

simplelayout.base
-----------------
* Base functions
* Base layout rendering
* Base block actions
* Base viewlets
  - one column
  - two columns
  - two columns with one column on top
  - controls
* configlet
  - simplelayout is completely configurable TTW, including image sizes and column dimensions 
* design menu
  - choose between the different designs/layouts 
* includes block configuration adapters
  - all block configs such as layout, image sizes, block height etc, will be saved in an adapter (annotations) for every block
* upgrade steps
* base JS functions
  - align to grid (for two columns designs only)
  - helper functions
* New scales for atct image field (requires zope restart)

For more information check simplelayout dependencies:
* simplelayout.ui.base
* simplelayout.types.common
* simplelayout.ui.dragndrop


FAQ
===

This FAQ provides some technical information/answers.

:Q: After reinstall I lose my configlet configuration?

:A: Do not reinstall simplelayout.base using QI, but rather use portal_setup import steps.
    Because the configlet data is stored in a local utility, in the event of a 
    reinstallation the utility will be removed (all data is gone) and added 
    again with default values. The following example shows how to change
    the sl configlet default values with setuphandlers in a policy package. 
  
    imports::

      from zope.component import getUtility
      from simplelayout.base.interfaces import IBlockConfig
      from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration
  
    config.py::

      SL_CONFIGURATION = {'same_workflow' : True,
                          'show_design_tab' : True,
                          'small_size' : 145,
                          'middle_size' : 302,
                          'full_size' : 614,
                          'small_size_two' : 66,
                          'middle_size_two' : 145,
                          'full_size_two' : 300}
  
    method in setuphandlers.py::

      def simplelayoutConf(self):
          sl_conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
          for key in SL_CONFIGURATION:
              setattr(sl_conf,key,SL_CONFIGURATION[key])
      

:Q: How does simplelayout know which content type is a block?
:A: Simplelayout marks blockable types with the interface *ISimpleLayoutBlock*

:Q: Can I use simplelayout listings on other content types?
:A: Of course, just make sure your type provides the ISimpleLayoutCapable
    interface and paste the following code into your template ::
    
      <tal:block content="structure provider:simplelayout.base.listing" />
    
    Make simplelayout blocks addable on your type. 

:Q: Can I uninstall simplelayout.base? 
:A: As many new packages based on component architecture, not yet...

:Q: How can I add a new image scale? 
:A: ...

:Q: How can i remove them?
:A: Navigate to portla_types/blocktype in the ZMI, select "actions" and 
    remove the image scale from actions list. 

:Q: I have a content type which I want to use it as block in simplelayout?
:A: Just register a BrowserView named block_view for the specific content type, 
    then z3c knows what to do. Example in simplelayout.types.common:
    
    configure.zcml::
    
      <browser:page
        for="Products.ATContentTypes.interface.file.IATFile"
        name="block_view"
        template="file.pt"
        class=".views.FileView"
        permission="zope2.View" />

:Q: I would like to create my own design template?
:A: ... 

:Q: Is there a possibility for blocks to show up as a portlet? 
:A: This feature is under development and will be released soon. 

:Q: How do you know in multible column designs, where to show up the blocks?
:A: Blocks has two additional interfaces: a slot interface and a column 
    interface. The slot interface tells the block where he should appear. 
    The column interface desides the image scale. 

:Q: Recalculation if all images takes a very long time?
:A: If you tick the box "Set simplelayout scales as image scales", the recalcultation
    can take a very long time, because it has to calculate a lot of new scales
    on every image. 

:Q: My images will be resized by CSS?
:A: Tick the box "Set simplelayout scales as image scales", restart zope an "recalc images". 
    Don't use atct_tool for this action, because it will ignore paragraphs. 

:Q: Is it possible to use more than one block_view per type?
:A: Yes, in the 2.0 release of simplelayout.base its possible to define your own view
    for a blockable type, you have to customize the actions and the action-icons of your 
    content type. the action id should look like the following example
    id: sl-dummyscale-dummycssklass-myview
    sl- = simplelayout prefix for actions
    dummyscale = the image scale, possible values are small, half or full 
    dummycssklass = an additional css wrapper class 
    myview = your view must be registered as block_view-myview 

    If yout don't need a scale or additional css class, please fill in some 
    dummy values as in the example above, Otherwise your view will have the
    wrong name. 

TODO
====

* TESTS
* mess up JS
* fix block height, if moving blocks from two to one column. 
* send feedback if ajax request fails


Copyright and credits
----------------------

simplelayout is copyright 2009 by 4teamwork_ , and is licensed under the GPL. See LICENSE.txt for details.

.. _4teamwork: http://www.4teamwork.ch/ 
