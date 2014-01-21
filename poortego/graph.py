# graph.py

#
# Poortego Graph
#  - Methods for accessing GraphDB
# 

###
# Good neo4j-Python References:
# - http://book.py2neo.org/en/latest/graphs_nodes_relationships/#nodes-relationships
# - http://blog.safaribooksonline.com/2013/07/23/using-neo4j-from-python/
# - http://blog.safaribooksonline.com/2013/08/07/managing-uniqueness-with-py2neo/
###

from py2neo import neo4j, node, rel

class Graph:
	"""Used for GraphDB interaction"""
	
	def __init__(self):
		"""Constructor, setup GraphDB connection"""
		self.graph_db = neo4j.GraphDatabaseService()
		self.set_defaults()

	def set_defaults(self):
		"""Create Default Poortego Nodes, Indexes, etc. if not exists"""
		node_name_index = self.graph_db.get_or_create_index(neo4j.Node, "Name")
		self.poortego_root_node = self.graph_db.get_or_create_indexed_node("Name", "name", "Poortego Root", {'name':'Poortego Root', 'type':'ROOT'})
	
	def PURGE(self):
		"""Delete everything from GraphDB -be sure you want to do this"""
		self.graph_db.clear()

	def get_graph_info(self):
		"""Return info dictionary about the GraphDB"""
		graph_info = {}
		graph_info["neo4j version"] = str(self.graph_db.neo4j_version)
		graph_info["Node count"] = str(self.graph_db.order)
		graph_info["Relationship count"] = str(self.graph_db.size)
		graph_info["Supports Index Uniqueness Modes"] = str(self.graph_db.supports_index_uniqueness_modes)
		graph_info["Supports Node Labels"] = str(self.graph_db.supports_node_labels)
		graph_info["Supports Schema Indexes"] = str(self.graph_db.supports_schema_indexes)
		return graph_info

	def show_types(self):
		"""Show node types"""
		node_types = set()
		rels = list(self.graph_db.match(start_node=self.poortego_root_node))
		for rel in rels:
			if "type" in rel.end_node:
				node_types.add(rel.end_node["type"])
		for t in sorted(set(node_types)):
			print t

	def show_nodes_to(self, end_node_id):
		"""Show nodes connected to end_node_id"""
		end_node_obj = self.graph_db.node(end_node_id)
		rels = list(self.graph_db.match(end_node=end_node_obj))
		for rel in rels:
			if "name" in rel.start_node:
				if "type" in rel.start_node:
					print str(rel.start_node._id) + ": " + str(rel.start_node["name"]) + "   [" + str(rel.start_node["type"]) + "]"


	def show_nodes_from(self, start_node_id):
		"""Show nodes connected from start_node_id"""
		start_node_obj = self.graph_db.node(start_node_id)
		rels = list(self.graph_db.match(start_node=start_node_obj))
		for rel in rels:
			if "name" in rel.end_node:
				if "type" in rel.end_node:
					print str(rel.end_node._id) + ": " + str(rel.end_node["name"]) + "   [" + str(rel.end_node["type"]) + "]"


        def get_nodes_by_property(self, prop="name"):
		"""Return node dictionary {id=>property value} for all nodes having the property key"""
                nodes = {} # id => property value
                rels = list(self.graph_db.match())
                for rel in rels:
                        if prop in rel.start_node:
				nodes[rel.start_node._id] = rel.start_node[prop]
                        if prop in rel.end_node:
				nodes[rel.end_node._id] = rel.end_node[prop]
                return nodes

        def get_all_rels(self):
		"""Return all relationships as dictionary {id=>relationship string representation}"""
                ret_rels = {} # id => relationship as string
                rels = list(self.graph_db.match())
                for rel in rels:
                        ret_rels[rel._id] = str(rel)
                return ret_rels

	def get_node_by_id(self, id_num):
		node = self.graph_db.node(id_num)
		node_dict = {'id':id_num, 'name':node['name']}
		return node_dict

	def create_node_from_dict(self, node_dict):
		"""Create and return node from dictionary containing node properties"""
		## Old shit ##
		#graph_node = self.graph_db.create(node_dict)
		#self.create_rel(self.graph_db.node(0), graph_node['type'], graph_node, {})
		#return graph_node
		##############

		#TODO: check for name/type within dict
		# Create New Node
		new_node = self.graph_db.get_or_create_indexed_node("Name", "name", node_dict['name'], node_dict)
		# Create Default Paths tying Node to root
		from_root_path = self.poortego_root_node.get_or_create_path(node_dict['type'], new_node)
		to_root_path = self.new_node.get_or_create_path("ROOT", self.poortego_root_node)
		return new_node

	def create_rel(self, graph_start_node, graph_end_node, rel_type, rel_prop_dict):
		"""Create and return relationship"""
		graph_rel = self.graph_db.create((graph_start_node, rel_type, graph_end_node, rel_prop_dict))
		return graph_rel
