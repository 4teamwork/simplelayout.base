import transaction
from plone.app.blob.migrations import migrate

def change_paragraph_image_storage_type_to_blobstorage(context):
    """Change the storagetype of the imagefield for paragraph"""

    print migrate(context, 'Paragraph')
    print migrate(context, 'News')
    transaction.commit()
