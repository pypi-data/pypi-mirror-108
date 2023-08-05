/** \file
 * Header file for the semantic tree node classes.
 */

#pragma once

#include <iostream>
#include "cqasm-tree.hpp"
#include "cqasm-primitives.hpp"
#include "cqasm-values.hpp"
#include "cqasm-error-model.hpp"
#include "cqasm-instruction.hpp"

namespace cqasm {

/**
 * Namespace for the semantic tree node classes.
 */
/**
 * \dot
 * digraph example {
 *   node [shape=record, fontname=Helvetica, fontsize=10];
 *   Annotated [ label="Annotated" URL="\ref cqasm::semantic::Annotated", style=dotted];
 *   AnnotationData [ label="AnnotationData" URL="\ref cqasm::semantic::AnnotationData"];
 *   Bundle [ label="Bundle" URL="\ref cqasm::semantic::Bundle"];
 *   ErrorModel [ label="ErrorModel" URL="\ref cqasm::semantic::ErrorModel"];
 *   Instruction [ label="Instruction" URL="\ref cqasm::semantic::Instruction"];
 *   Mapping [ label="Mapping" URL="\ref cqasm::semantic::Mapping"];
 *   Program [ label="Program" URL="\ref cqasm::semantic::Program"];
 *   Subcircuit [ label="Subcircuit" URL="\ref cqasm::semantic::Subcircuit"];
 *   Variable [ label="Variable" URL="\ref cqasm::semantic::Variable"];
 *   Version [ label="Version" URL="\ref cqasm::semantic::Version"];
 *   Annotated -> Bundle [ arrowhead=open, style=dotted ];
 *   Annotated -> ErrorModel [ arrowhead=open, style=dotted ];
 *   Annotated -> Instruction [ arrowhead=open, style=dotted ];
 *   Annotated -> Mapping [ arrowhead=open, style=dotted ];
 *   Annotated -> Subcircuit [ arrowhead=open, style=dotted ];
 *   Annotated -> Variable [ arrowhead=open, style=dotted ];
 *   Annotated -> AnnotationData [ label="annotations*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   prim0 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   AnnotationData -> prim0 [ label="interface", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim1 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   AnnotationData -> prim1 [ label="operation", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim2 [ label="values::Node" URL="\ref cqasm::values::Node"];
 *   AnnotationData -> prim2 [ label="operands*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   Bundle -> Instruction [ label="items+", arrowhead=normal, style=bold, fontname=Helvetica, fontsize=10];
 *   prim3 [ label="error_model::ErrorModelRef" URL="\ref cqasm::error_model::ErrorModelRef"];
 *   ErrorModel -> prim3 [ label="model", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim4 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   ErrorModel -> prim4 [ label="name", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim5 [ label="values::Node" URL="\ref cqasm::values::Node"];
 *   ErrorModel -> prim5 [ label="parameters*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   prim6 [ label="instruction::InstructionRef" URL="\ref cqasm::instruction::InstructionRef"];
 *   Instruction -> prim6 [ label="instruction", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim7 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   Instruction -> prim7 [ label="name", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim8 [ label="values::Node" URL="\ref cqasm::values::Node"];
 *   Instruction -> prim8 [ label="condition", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim9 [ label="values::Node" URL="\ref cqasm::values::Node"];
 *   Instruction -> prim9 [ label="operands*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   prim10 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   Mapping -> prim10 [ label="name", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim11 [ label="values::Node" URL="\ref cqasm::values::Node"];
 *   Mapping -> prim11 [ label="value", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   Program -> Version [ label="version", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim12 [ label="primitives::Int" URL="\ref cqasm::primitives::Int"];
 *   Program -> prim12 [ label="num_qubits", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   Program -> ErrorModel [ label="error_model?", arrowhead=open, style=solid, fontname=Helvetica, fontsize=10];
 *   Program -> Subcircuit [ label="subcircuits*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   Program -> Mapping [ label="mappings*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   Program -> Variable [ label="variables*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   prim13 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   Subcircuit -> prim13 [ label="name", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim14 [ label="primitives::Int" URL="\ref cqasm::primitives::Int"];
 *   Subcircuit -> prim14 [ label="iterations", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   Subcircuit -> Bundle [ label="bundles*", arrowhead=open, style=bold, fontname=Helvetica, fontsize=10];
 *   prim15 [ label="primitives::Str" URL="\ref cqasm::primitives::Str"];
 *   Variable -> prim15 [ label="name", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim16 [ label="types::Node" URL="\ref cqasm::types::Node"];
 *   Variable -> prim16 [ label="typ", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 *   prim17 [ label="primitives::Version" URL="\ref cqasm::primitives::Version"];
 *   Version -> prim17 [ label="items", arrowhead=normal, style=solid, fontname=Helvetica, fontsize=10];
 * }
 * \enddot
 */
namespace semantic {

// Base classes used to construct the tree.
using Base = cqasm::tree::Base;
template <class T> using Maybe   = cqasm::tree::Maybe<T>;
template <class T> using One     = cqasm::tree::One<T>;
template <class T> using Any     = cqasm::tree::Any<T>;
template <class T> using Many    = cqasm::tree::Many<T>;
template <class T> using OptLink = cqasm::tree::OptLink<T>;
template <class T> using Link    = cqasm::tree::Link<T>;

// Forward declarations for all classes.
class Node;
class Annotated;
class AnnotationData;
class Bundle;
class ErrorModel;
class Instruction;
class Mapping;
class Program;
class Subcircuit;
class Variable;
class Version;
class VisitorBase;
template <typename T = void>
class Visitor;
class RecursiveVisitor;
class Dumper;

/**
 * Enumeration of all node types.
 */
enum class NodeType {
    AnnotationData,
    Bundle,
    ErrorModel,
    Instruction,
    Mapping,
    Program,
    Subcircuit,
    Variable,
    Version
};

/**
 * Main class for all nodes.
 */
class Node : public Base {
public:

    /**
     * Returns the `NodeType` of this node.
     */
    virtual NodeType type() const = 0;

    /**
     * Returns a shallow copy of this node.
     */
    virtual One<Node> copy() const = 0;

    /**
     * Returns a deep copy of this node.
     */
    virtual One<Node> clone() const = 0;

    /**
     * Equality operator. Ignores annotations!
     */
    virtual bool operator==(const Node& rhs) const = 0;

    /**
     * Inequality operator. Ignores annotations!
     */
    inline bool operator!=(const Node& rhs) const {
        return !(*this == rhs);
    }

protected:

    /**
     * Internal helper method for visiter pattern.
     */
    virtual void visit_internal(VisitorBase &visitor, void *retval=nullptr) = 0;

public:

    /**
     * Visit this object.
     */
    template <typename T>
    T visit(Visitor<T> &visitor);

    /**
     * Writes a debug dump of this node to the given stream.
     */
    void dump(std::ostream &out=std::cout, int indent=0);

    /**
     * Interprets this node to a node of type Annotated. Returns null if it has
     * the wrong type.
     */
    virtual Annotated *as_annotated();

    /**
     * Interprets this node to a node of type Annotated. Returns null if it has
     * the wrong type.
     */
    virtual const Annotated *as_annotated() const;

    /**
     * Interprets this node to a node of type AnnotationData. Returns null if it
     * has the wrong type.
     */
    virtual AnnotationData *as_annotation_data();

    /**
     * Interprets this node to a node of type AnnotationData. Returns null if it
     * has the wrong type.
     */
    virtual const AnnotationData *as_annotation_data() const;

    /**
     * Interprets this node to a node of type Bundle. Returns null if it has the
     * wrong type.
     */
    virtual Bundle *as_bundle();

    /**
     * Interprets this node to a node of type Bundle. Returns null if it has the
     * wrong type.
     */
    virtual const Bundle *as_bundle() const;

    /**
     * Interprets this node to a node of type ErrorModel. Returns null if it has
     * the wrong type.
     */
    virtual ErrorModel *as_error_model();

    /**
     * Interprets this node to a node of type ErrorModel. Returns null if it has
     * the wrong type.
     */
    virtual const ErrorModel *as_error_model() const;

    /**
     * Interprets this node to a node of type Instruction. Returns null if it
     * has the wrong type.
     */
    virtual Instruction *as_instruction();

    /**
     * Interprets this node to a node of type Instruction. Returns null if it
     * has the wrong type.
     */
    virtual const Instruction *as_instruction() const;

    /**
     * Interprets this node to a node of type Mapping. Returns null if it has
     * the wrong type.
     */
    virtual Mapping *as_mapping();

    /**
     * Interprets this node to a node of type Mapping. Returns null if it has
     * the wrong type.
     */
    virtual const Mapping *as_mapping() const;

    /**
     * Interprets this node to a node of type Program. Returns null if it has
     * the wrong type.
     */
    virtual Program *as_program();

    /**
     * Interprets this node to a node of type Program. Returns null if it has
     * the wrong type.
     */
    virtual const Program *as_program() const;

    /**
     * Interprets this node to a node of type Subcircuit. Returns null if it has
     * the wrong type.
     */
    virtual Subcircuit *as_subcircuit();

    /**
     * Interprets this node to a node of type Subcircuit. Returns null if it has
     * the wrong type.
     */
    virtual const Subcircuit *as_subcircuit() const;

    /**
     * Interprets this node to a node of type Variable. Returns null if it has
     * the wrong type.
     */
    virtual Variable *as_variable();

    /**
     * Interprets this node to a node of type Variable. Returns null if it has
     * the wrong type.
     */
    virtual const Variable *as_variable() const;

    /**
     * Interprets this node to a node of type Version. Returns null if it has
     * the wrong type.
     */
    virtual Version *as_version();

    /**
     * Interprets this node to a node of type Version. Returns null if it has
     * the wrong type.
     */
    virtual const Version *as_version() const;

};

/**
 * Represents a node that carries annotation data.
 */
class Annotated : public Node {
public:

    /**
     * Zero or more annotations attached to this object.
     */
    Any<AnnotationData> annotations;

    /**
     * Constructor.
     */
    Annotated(const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Interprets this node to a node of type Annotated. Returns null if it has
     * the wrong type.
     */
    Annotated *as_annotated() override;

    /**
     * Interprets this node to a node of type Annotated. Returns null if it has
     * the wrong type.
     */
    const Annotated *as_annotated() const override;

};

/**
 * Represents an annotation.
 */
class AnnotationData : public Node {
public:

    /**
     * The interface this annotation is intended for. If a target doesn't
     * support an interface, it should silently ignore the annotation.
     */
    cqasm::primitives::Str interface;

    /**
     * The operation within the interface that this annotation is intended for.
     * If a supports the corresponding interface but not the operation, it
     * should throw an error.
     */
    cqasm::primitives::Str operation;

    /**
     * Any operands attached to the annotation.
     */
    Any<cqasm::values::Node> operands;

    /**
     * Constructor.
     */
    AnnotationData(const cqasm::primitives::Str &interface = cqasm::primitives::initialize<cqasm::primitives::Str>(), const cqasm::primitives::Str &operation = cqasm::primitives::initialize<cqasm::primitives::Str>(), const Any<cqasm::values::Node> &operands = cqasm::primitives::initialize<Any<cqasm::values::Node>>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `AnnotationData` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type AnnotationData. Returns null if it
     * has the wrong type.
     */
    AnnotationData *as_annotation_data() override;

    /**
     * Interprets this node to a node of type AnnotationData. Returns null if it
     * has the wrong type.
     */
    const AnnotationData *as_annotation_data() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * A bundle of instructions, to be executed in parallel.
 */
class Bundle : public Annotated {
public:

    /**
     * The list of parallel instructions.
     */
    Many<Instruction> items;

    /**
     * Constructor.
     */
    Bundle(const Many<Instruction> &items = Many<Instruction>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Bundle` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Bundle. Returns null if it has the
     * wrong type.
     */
    Bundle *as_bundle() override;

    /**
     * Interprets this node to a node of type Bundle. Returns null if it has the
     * wrong type.
     */
    const Bundle *as_bundle() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * Error model information.
 */
class ErrorModel : public Annotated {
public:

    /**
     * Error model type as registered through the API.
     */
    cqasm::error_model::ErrorModelRef model;

    /**
     * Name as it appears in the cQASM file.
     */
    cqasm::primitives::Str name;

    /**
     * Error model parameters.
     */
    Any<cqasm::values::Node> parameters;

    /**
     * Constructor.
     */
    ErrorModel(const cqasm::error_model::ErrorModelRef &model = cqasm::primitives::initialize<cqasm::error_model::ErrorModelRef>(), const cqasm::primitives::Str &name = cqasm::primitives::initialize<cqasm::primitives::Str>(), const Any<cqasm::values::Node> &parameters = cqasm::primitives::initialize<Any<cqasm::values::Node>>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `ErrorModel` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type ErrorModel. Returns null if it has
     * the wrong type.
     */
    ErrorModel *as_error_model() override;

    /**
     * Interprets this node to a node of type ErrorModel. Returns null if it has
     * the wrong type.
     */
    const ErrorModel *as_error_model() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * An instruction (a.k.a. gate).
 */
class Instruction : public Annotated {
public:

    /**
     * Instruction type as registered through the API.
     */
    cqasm::instruction::InstructionRef instruction;

    /**
     * Name as it appears in the cQASM file.
     */
    cqasm::primitives::Str name;

    /**
     * Condition (c- notation). When there is no condition, this is a constant
     * boolean set to true.
     */
    One<cqasm::values::Node> condition;

    /**
     * Operands for the instruction.
     */
    Any<cqasm::values::Node> operands;

    /**
     * Constructor.
     */
    Instruction(const cqasm::instruction::InstructionRef &instruction = cqasm::primitives::initialize<cqasm::instruction::InstructionRef>(), const cqasm::primitives::Str &name = cqasm::primitives::initialize<cqasm::primitives::Str>(), const One<cqasm::values::Node> &condition = cqasm::primitives::initialize<One<cqasm::values::Node>>(), const Any<cqasm::values::Node> &operands = cqasm::primitives::initialize<Any<cqasm::values::Node>>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Instruction` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Instruction. Returns null if it
     * has the wrong type.
     */
    Instruction *as_instruction() override;

    /**
     * Interprets this node to a node of type Instruction. Returns null if it
     * has the wrong type.
     */
    const Instruction *as_instruction() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * A mapping. That is, a user-defined identifier mapping to some value.
 */
class Mapping : public Annotated {
public:

    /**
     * The name of the mapping.
     */
    cqasm::primitives::Str name;

    /**
     * The value it maps to.
     */
    One<cqasm::values::Node> value;

    /**
     * Constructor.
     */
    Mapping(const cqasm::primitives::Str &name = cqasm::primitives::initialize<cqasm::primitives::Str>(), const One<cqasm::values::Node> &value = cqasm::primitives::initialize<One<cqasm::values::Node>>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Mapping` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Mapping. Returns null if it has
     * the wrong type.
     */
    Mapping *as_mapping() override;

    /**
     * Interprets this node to a node of type Mapping. Returns null if it has
     * the wrong type.
     */
    const Mapping *as_mapping() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * A complete program.
 */
class Program : public Node {
public:

    /**
     * File version.
     */
    One<Version> version;

    /**
     * The required qubit register size.
     */
    cqasm::primitives::Int num_qubits;

    /**
     * Error model information.
     */
    Maybe<ErrorModel> error_model;

    /**
     * The list of subcircuit.
     */
    Any<Subcircuit> subcircuits;

    /**
     * The list of all user-defined mappings after parsing.
     */
    Any<Mapping> mappings;

    /**
     * This list of all user-defined variables at any point in the code.
     */
    Any<Variable> variables;

    /**
     * Constructor.
     */
    Program(const One<Version> &version = One<Version>(), const cqasm::primitives::Int &num_qubits = cqasm::primitives::initialize<cqasm::primitives::Int>(), const Maybe<ErrorModel> &error_model = Maybe<ErrorModel>(), const Any<Subcircuit> &subcircuits = Any<Subcircuit>(), const Any<Mapping> &mappings = Any<Mapping>(), const Any<Variable> &variables = Any<Variable>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Program` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Program. Returns null if it has
     * the wrong type.
     */
    Program *as_program() override;

    /**
     * Interprets this node to a node of type Program. Returns null if it has
     * the wrong type.
     */
    const Program *as_program() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * A subcircuit. That is, a named collection of bundles, possibly repeated a
 * number of times.
 */
class Subcircuit : public Annotated {
public:

    /**
     * The name of the subcircuit. If the file doesn't start with a subcircuit
     * definition, this is empty for the first subcircuit.
     */
    cqasm::primitives::Str name;

    /**
     * An optional integer expression representing the number of iterations for
     * this subcircuit. This is 1 when the iteration count is not specified.
     */
    cqasm::primitives::Int iterations;

    /**
     * The instruction bundles contained by this subcircuit.
     */
    Any<Bundle> bundles;

    /**
     * Constructor.
     */
    Subcircuit(const cqasm::primitives::Str &name = cqasm::primitives::initialize<cqasm::primitives::Str>(), const cqasm::primitives::Int &iterations = cqasm::primitives::initialize<cqasm::primitives::Int>(), const Any<Bundle> &bundles = Any<Bundle>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Subcircuit` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Subcircuit. Returns null if it has
     * the wrong type.
     */
    Subcircuit *as_subcircuit() override;

    /**
     * Interprets this node to a node of type Subcircuit. Returns null if it has
     * the wrong type.
     */
    const Subcircuit *as_subcircuit() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * A variable.
 */
class Variable : public Annotated {
public:

    /**
     * The name of the variable.
     */
    cqasm::primitives::Str name;

    /**
     * The type of the variable.
     */
    One<cqasm::types::Node> typ;

    /**
     * Constructor.
     */
    Variable(const cqasm::primitives::Str &name = cqasm::primitives::initialize<cqasm::primitives::Str>(), const One<cqasm::types::Node> &typ = cqasm::primitives::initialize<One<cqasm::types::Node>>(), const Any<AnnotationData> &annotations = Any<AnnotationData>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Variable` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Variable. Returns null if it has
     * the wrong type.
     */
    Variable *as_variable() override;

    /**
     * Interprets this node to a node of type Variable. Returns null if it has
     * the wrong type.
     */
    const Variable *as_variable() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * The file version identifier.
 */
class Version : public Node {
public:

    /**
     * The list of version components, ordered major to minor.
     */
    cqasm::primitives::Version items;

    /**
     * Constructor.
     */
    Version(const cqasm::primitives::Version &items = cqasm::primitives::initialize<cqasm::primitives::Version>());

    /**
     * Registers all reachable nodes with the given PointerMap.
     */
    void find_reachable(::tree::base::PointerMap &map) const override;

    /**
     * Returns whether this `Version` is complete/fully defined.
     */
    void check_complete(const ::tree::base::PointerMap &map) const override;

    /**
     * Returns the `NodeType` of this node.
     */
    NodeType type() const override;

protected:

    /**
     * Helper method for visiting nodes.
     */
    void visit_internal(VisitorBase &visitor, void *retval) override;

public:

    /**
     * Interprets this node to a node of type Version. Returns null if it has
     * the wrong type.
     */
    Version *as_version() override;

    /**
     * Interprets this node to a node of type Version. Returns null if it has
     * the wrong type.
     */
    const Version *as_version() const override;

    /**
     * Returns a shallow copy of this node.
     */
    One<Node> copy() const override;

    /**
     * Returns a deep copy of this node.
     */
    One<Node> clone() const override;

    /**
     * Equality operator. Ignores annotations!
     */
    bool operator==(const Node& rhs) const override;

};

/**
 * Internal class for implementing the visitor pattern.
 */
class VisitorBase {
public:

    /**
     * Virtual destructor for proper cleanup.
     */
    virtual ~VisitorBase() = default;

protected:

    friend class Node;
    friend class Annotated;
    friend class AnnotationData;
    friend class Bundle;
    friend class ErrorModel;
    friend class Instruction;
    friend class Mapping;
    friend class Program;
    friend class Subcircuit;
    friend class Variable;
    friend class Version;

    /**
     * Internal visitor function for nodes of any type.
     */
    virtual void raw_visit_node(Node &node, void *retval) = 0;

    /**
     * Internal visitor function for `Annotated` nodes.
     */
    virtual void raw_visit_annotated(Annotated &node, void *retval) = 0;

    /**
     * Internal visitor function for `AnnotationData` nodes.
     */
    virtual void raw_visit_annotation_data(AnnotationData &node, void *retval) = 0;

    /**
     * Internal visitor function for `Bundle` nodes.
     */
    virtual void raw_visit_bundle(Bundle &node, void *retval) = 0;

    /**
     * Internal visitor function for `ErrorModel` nodes.
     */
    virtual void raw_visit_error_model(ErrorModel &node, void *retval) = 0;

    /**
     * Internal visitor function for `Instruction` nodes.
     */
    virtual void raw_visit_instruction(Instruction &node, void *retval) = 0;

    /**
     * Internal visitor function for `Mapping` nodes.
     */
    virtual void raw_visit_mapping(Mapping &node, void *retval) = 0;

    /**
     * Internal visitor function for `Program` nodes.
     */
    virtual void raw_visit_program(Program &node, void *retval) = 0;

    /**
     * Internal visitor function for `Subcircuit` nodes.
     */
    virtual void raw_visit_subcircuit(Subcircuit &node, void *retval) = 0;

    /**
     * Internal visitor function for `Variable` nodes.
     */
    virtual void raw_visit_variable(Variable &node, void *retval) = 0;

    /**
     * Internal visitor function for `Version` nodes.
     */
    virtual void raw_visit_version(Version &node, void *retval) = 0;

};

/**
 * Base class for the visitor pattern for the tree.
 * 
 * To operate on the tree, derive from this class, describe your operation by
 * overriding the appropriate visit functions. and then call
 * `node->visit(your_visitor)`. The default implementations for the
 * node-specific functions fall back to the more generic functions, eventually
 * leading to `visit_node()`, which must be implemented with the desired
 * behavior for unknown nodes.
 */
template <typename T>
class Visitor : public VisitorBase {
protected:

    /**
     * Internal visitor function for nodes of any type.
     */
    void raw_visit_node(Node &node, void *retval) override;

    /**
     * Internal visitor function for `Annotated` nodes.
     */
    void raw_visit_annotated(Annotated &node, void *retval) override;

    /**
     * Internal visitor function for `AnnotationData` nodes.
     */
    void raw_visit_annotation_data(AnnotationData &node, void *retval) override;

    /**
     * Internal visitor function for `Bundle` nodes.
     */
    void raw_visit_bundle(Bundle &node, void *retval) override;

    /**
     * Internal visitor function for `ErrorModel` nodes.
     */
    void raw_visit_error_model(ErrorModel &node, void *retval) override;

    /**
     * Internal visitor function for `Instruction` nodes.
     */
    void raw_visit_instruction(Instruction &node, void *retval) override;

    /**
     * Internal visitor function for `Mapping` nodes.
     */
    void raw_visit_mapping(Mapping &node, void *retval) override;

    /**
     * Internal visitor function for `Program` nodes.
     */
    void raw_visit_program(Program &node, void *retval) override;

    /**
     * Internal visitor function for `Subcircuit` nodes.
     */
    void raw_visit_subcircuit(Subcircuit &node, void *retval) override;

    /**
     * Internal visitor function for `Variable` nodes.
     */
    void raw_visit_variable(Variable &node, void *retval) override;

    /**
     * Internal visitor function for `Version` nodes.
     */
    void raw_visit_version(Version &node, void *retval) override;

public:

    /**
     * Fallback function for nodes of any type.
     */
    virtual T visit_node(Node &node) = 0;

    /**
     * Fallback function for `Annotated` nodes.
     */
    virtual T visit_annotated(Annotated &node) {
        return visit_node(node);
    }

    /**
     * Visitor function for `AnnotationData` nodes.
     */
    virtual T visit_annotation_data(AnnotationData &node) {
        return visit_node(node);
    }

    /**
     * Visitor function for `Bundle` nodes.
     */
    virtual T visit_bundle(Bundle &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `ErrorModel` nodes.
     */
    virtual T visit_error_model(ErrorModel &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `Instruction` nodes.
     */
    virtual T visit_instruction(Instruction &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `Mapping` nodes.
     */
    virtual T visit_mapping(Mapping &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `Program` nodes.
     */
    virtual T visit_program(Program &node) {
        return visit_node(node);
    }

    /**
     * Visitor function for `Subcircuit` nodes.
     */
    virtual T visit_subcircuit(Subcircuit &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `Variable` nodes.
     */
    virtual T visit_variable(Variable &node) {
        return visit_annotated(node);
    }

    /**
     * Visitor function for `Version` nodes.
     */
    virtual T visit_version(Version &node) {
        return visit_node(node);
    }

};

    /**
     * Internal visitor function for nodes of any type.
     */
    template <typename T>
    void Visitor<T>::raw_visit_node(Node &node, void *retval) {
        if (retval == nullptr) {
            this->visit_node(node);
        } else {
            *((T*)retval) = this->visit_node(node);
        };
    }

    /**
     * Internal visitor function for nodes of any type.
     */
    template <>
    void Visitor<void>::raw_visit_node(Node &node, void *retval);

    /**
     * Internal visitor function for `Annotated` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_annotated(Annotated &node, void *retval) {
        if (retval == nullptr) {
            this->visit_annotated(node);
        } else {
            *((T*)retval) = this->visit_annotated(node);
        };
    }

    /**
     * Internal visitor function for `Annotated` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_annotated(Annotated &node, void *retval);

    /**
     * Internal visitor function for `AnnotationData` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_annotation_data(AnnotationData &node, void *retval) {
        if (retval == nullptr) {
            this->visit_annotation_data(node);
        } else {
            *((T*)retval) = this->visit_annotation_data(node);
        };
    }

    /**
     * Internal visitor function for `AnnotationData` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_annotation_data(AnnotationData &node, void *retval);

    /**
     * Internal visitor function for `Bundle` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_bundle(Bundle &node, void *retval) {
        if (retval == nullptr) {
            this->visit_bundle(node);
        } else {
            *((T*)retval) = this->visit_bundle(node);
        };
    }

    /**
     * Internal visitor function for `Bundle` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_bundle(Bundle &node, void *retval);

    /**
     * Internal visitor function for `ErrorModel` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_error_model(ErrorModel &node, void *retval) {
        if (retval == nullptr) {
            this->visit_error_model(node);
        } else {
            *((T*)retval) = this->visit_error_model(node);
        };
    }

    /**
     * Internal visitor function for `ErrorModel` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_error_model(ErrorModel &node, void *retval);

    /**
     * Internal visitor function for `Instruction` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_instruction(Instruction &node, void *retval) {
        if (retval == nullptr) {
            this->visit_instruction(node);
        } else {
            *((T*)retval) = this->visit_instruction(node);
        };
    }

    /**
     * Internal visitor function for `Instruction` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_instruction(Instruction &node, void *retval);

    /**
     * Internal visitor function for `Mapping` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_mapping(Mapping &node, void *retval) {
        if (retval == nullptr) {
            this->visit_mapping(node);
        } else {
            *((T*)retval) = this->visit_mapping(node);
        };
    }

    /**
     * Internal visitor function for `Mapping` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_mapping(Mapping &node, void *retval);

    /**
     * Internal visitor function for `Program` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_program(Program &node, void *retval) {
        if (retval == nullptr) {
            this->visit_program(node);
        } else {
            *((T*)retval) = this->visit_program(node);
        };
    }

    /**
     * Internal visitor function for `Program` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_program(Program &node, void *retval);

    /**
     * Internal visitor function for `Subcircuit` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_subcircuit(Subcircuit &node, void *retval) {
        if (retval == nullptr) {
            this->visit_subcircuit(node);
        } else {
            *((T*)retval) = this->visit_subcircuit(node);
        };
    }

    /**
     * Internal visitor function for `Subcircuit` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_subcircuit(Subcircuit &node, void *retval);

    /**
     * Internal visitor function for `Variable` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_variable(Variable &node, void *retval) {
        if (retval == nullptr) {
            this->visit_variable(node);
        } else {
            *((T*)retval) = this->visit_variable(node);
        };
    }

    /**
     * Internal visitor function for `Variable` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_variable(Variable &node, void *retval);

    /**
     * Internal visitor function for `Version` nodes.
     */
    template <typename T>
    void Visitor<T>::raw_visit_version(Version &node, void *retval) {
        if (retval == nullptr) {
            this->visit_version(node);
        } else {
            *((T*)retval) = this->visit_version(node);
        };
    }

    /**
     * Internal visitor function for `Version` nodes.
     */
    template <>
    void Visitor<void>::raw_visit_version(Version &node, void *retval);

/**
 * Visitor base class defaulting to DFS traversal.
 * 
 * The visitor functions for nodes with subnode fields default to DFS traversal
 * instead of falling back to more generic node types.
 */
class RecursiveVisitor : public Visitor<void> {
public:

    /**
     * Recursive traversal for `Annotated` nodes.
     */
    void visit_annotated(Annotated &node) override;

    /**
     * Recursive traversal for `Bundle` nodes.
     */
    void visit_bundle(Bundle &node) override;

    /**
     * Recursive traversal for `ErrorModel` nodes.
     */
    void visit_error_model(ErrorModel &node) override;

    /**
     * Recursive traversal for `Instruction` nodes.
     */
    void visit_instruction(Instruction &node) override;

    /**
     * Recursive traversal for `Mapping` nodes.
     */
    void visit_mapping(Mapping &node) override;

    /**
     * Recursive traversal for `Program` nodes.
     */
    void visit_program(Program &node) override;

    /**
     * Recursive traversal for `Subcircuit` nodes.
     */
    void visit_subcircuit(Subcircuit &node) override;

    /**
     * Recursive traversal for `Variable` nodes.
     */
    void visit_variable(Variable &node) override;

};

/**
 * Visitor class that debug-dumps a tree to a stream
 */
class Dumper : public RecursiveVisitor {
protected:

    /**
     * Output stream to dump to.
     */
    std::ostream &out;

    /**
     * Current indentation level.
     */
    int indent = 0;

    /**
     * Whether we're printing the contents of a link.
     */
    bool in_link = false;

    /**
     * Writes the current indentation level's worth of spaces.
     */
    void write_indent();

public:

    /**
     * Construct a dumping visitor.
     */
    Dumper(std::ostream &out, int indent=0) : out(out), indent(indent) {};

    /**
     * Dumps a `Node`.
     */
    void visit_node(Node &node) override;
    /**
     * Dumps a `Annotated` node.
     */
    void visit_annotated(Annotated &node) override;

    /**
     * Dumps a `AnnotationData` node.
     */
    void visit_annotation_data(AnnotationData &node) override;

    /**
     * Dumps a `Bundle` node.
     */
    void visit_bundle(Bundle &node) override;

    /**
     * Dumps a `ErrorModel` node.
     */
    void visit_error_model(ErrorModel &node) override;

    /**
     * Dumps a `Instruction` node.
     */
    void visit_instruction(Instruction &node) override;

    /**
     * Dumps a `Mapping` node.
     */
    void visit_mapping(Mapping &node) override;

    /**
     * Dumps a `Program` node.
     */
    void visit_program(Program &node) override;

    /**
     * Dumps a `Subcircuit` node.
     */
    void visit_subcircuit(Subcircuit &node) override;

    /**
     * Dumps a `Variable` node.
     */
    void visit_variable(Variable &node) override;

    /**
     * Dumps a `Version` node.
     */
    void visit_version(Version &node) override;

};

/**
 * Visit this object.
 */
template <typename T>
T Node::visit(Visitor<T> &visitor) {
    T retval;
    this->visit_internal(visitor, &retval);
    return retval;
}

/**
 * Visit this object.
 */
template <>
void Node::visit(Visitor<void> &visitor);

/**
 * Stream << overload for tree nodes (writes debug dump).
 */
std::ostream &operator<<(std::ostream &os, const Node &object);

} // namespace semantic
} // namespace cqasm

