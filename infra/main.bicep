// Placeholder for Azure Bicep deployment

param location string = 'eastus'

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-06-01' = {
  name: 'akudaikonstorage'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}