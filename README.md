# Ballatrix Metadata

This is a microservice extending the storage database managed by `bellastore` with metadata.

This is achieved by creating metadata tables always following the relational principle of holding key value pairs, where
the key points to the foreign key being a hash held by the main storage table.

