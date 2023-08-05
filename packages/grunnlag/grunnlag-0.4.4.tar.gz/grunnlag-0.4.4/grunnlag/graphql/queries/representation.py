

from bergen.query import DelayedGQL


FILTER_REPRESENTATION = DelayedGQL("""
query Representation($name: String) {
  representations(name: $name) {
    id
    name
    store
    variety
    tags
    unique
    sample {
      id
    }
  }
}
""")

GET_REPRESENTATION = DelayedGQL("""
query Representation($id: ID!){
  representation(id: $id){
    id
    name
    tags
    variety
    store
    unique
    sample {
      id
    }
  
  }
}
""")