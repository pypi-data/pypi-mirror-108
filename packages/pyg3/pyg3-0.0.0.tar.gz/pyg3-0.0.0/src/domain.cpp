#include <pybind11/pybind11.h>
#include <domain/domain/Domain.h>
#include <domain/domain/Element.h>
#include <domain/node/Node.h>

/* Error streams */
#include <handler/OPS_Stream.h>
#include <StandardStream.h>

/* Create global error stream */
StandardStream sserr;
OPS_Stream *opserrPtr = &sserr;

namespace py = pybind11;

// py::module pyg3_domain = m.def_submodule("domain", "Domain objects");

PYBIND11_MODULE (domain, m)
{
    py::class_ < Domain > (m, "Domain")
        .def (py::init())
        .def ("addNode", &Domain::addNode)
        .def ("getNode", &Domain::getNode)

        .def ("getElement", &Domain::getElement)
    ;

    py::class_ < Node > (m, "Node")
        .def (py::init<int, int, float, float> (),
             py::arg("tag"), py::arg("ndof"), py::arg("Crd1"), py::arg("Crd2")
        )
        .def ("getNumberDOF", &Node::getNumberDOF)
        .def ("getDisp", &Node::getDisp)
    ;
}
