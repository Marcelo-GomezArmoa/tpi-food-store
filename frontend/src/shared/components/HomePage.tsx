/**
 * Página de Inicio
 * Pantalla de bienvenida al sistema Food Store
 */

import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <div
      className="min-h-screen"
      style={{
        backgroundImage: "linear-gradient(to bottom, #eff6ff, #dbeafe)",
      }}
    >
      <div className="max-w-4xl mx-auto px-4 py-16 sm:px-6 lg:px-8">
        {/* Contenedor Principal */}
        <div className="text-center space-y-8">
          {/* Encabezado */}
          <div className="space-y-4">
            <h1 className="text-5xl font-bold text-gray-900">
              🍕 Bienvenido a Food Store UTN
            </h1>
            <p className="text-xl text-gray-600">
              Unidad 7 - Proyecto Full Stack
            </p>
          </div>

          {/* Descripción */}
          <div className="bg-white rounded-lg shadow-lg p-8 space-y-4">
            <h2 className="text-2xl font-semibold text-gray-800">
              Sistema de Gestión de Productos y Categorías
            </h2>
            <p className="text-gray-700 leading-relaxed">
              Una aplicación Full Stack moderna que demuestra la integración de tecnologías
              contemporáneas en desarrollo web. Este proyecto combina un robusto backend con
              FastAPI y SQLModel, con un frontend interactivo construido con React y TypeScript.
            </p>
          </div>

          {/* Stack Tecnológico */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Backend */}
            <div
              className="rounded-lg p-6 shadow-md"
              style={{
                backgroundImage:
                  "linear-gradient(to bottom right, #faf5ff, #f3e8ff)",
              }}
            >
              <h3 className="text-xl font-bold text-purple-900 mb-4">Backend</h3>
              <ul className="space-y-2 text-left">
                <li className="flex items-center gap-2 text-purple-800">
                  <span className="text-lg">⚡</span>
                  <span>FastAPI - Framework web moderno</span>
                </li>
                <li className="flex items-center gap-2 text-purple-800">
                  <span className="text-lg">📊</span>
                  <span>SQLModel - ORM con SQLAlchemy</span>
                </li>
                <li className="flex items-center gap-2 text-purple-800">
                  <span className="text-lg">🐍</span>
                  <span>Python 3.10+ - Tipado fuerte</span>
                </li>
                <li className="flex items-center gap-2 text-purple-800">
                  <span className="text-lg">🗄️</span>
                  <span>PostgreSQL - Base de datos relacional</span>
                </li>
              </ul>
            </div>

            {/* Frontend */}
            <div
              className="rounded-lg p-6 shadow-md"
              style={{
                backgroundImage:
                  "linear-gradient(to bottom right, #eff6ff, #dbeafe)",
              }}
            >
              <h3 className="text-xl font-bold text-blue-900 mb-4">Frontend</h3>
              <ul className="space-y-2 text-left">
                <li className="flex items-center gap-2 text-blue-800">
                  <span className="text-lg">⚛️</span>
                  <span>React 19+ - Interfaz de usuario</span>
                </li>
                <li className="flex items-center gap-2 text-blue-800">
                  <span className="text-lg">🔷</span>
                  <span>TypeScript - Tipado estático</span>
                </li>
                <li className="flex items-center gap-2 text-blue-800">
                  <span className="text-lg">🎨</span>
                  <span>Tailwind CSS - Estilos modernos</span>
                </li>
                <li className="flex items-center gap-2 text-blue-800">
                  <span className="text-lg">🔄</span>
                  <span>TanStack Query - Estado y caché</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Características */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Características</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ CRUD Completo</p>
                <p className="text-sm text-blue-800">
                  Gestión total de productos y categorías
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ Relaciones M2M</p>
                <p className="text-sm text-blue-800">
                  Asociación entre productos y categorías
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ API RESTful</p>
                <p className="text-sm text-blue-800">
                  Endpoints documentados y tipados
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ Tipado Fuerte</p>
                <p className="text-sm text-blue-800">
                  TypeScript en backend y frontend
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ Manejo de Errores</p>
                <p className="text-sm text-blue-800">
                  Excepciones y validaciones robustas
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="font-semibold text-blue-900 mb-2">✓ Interfaz Moderna</p>
                <p className="text-sm text-blue-800">
                  Diseño limpio y responsive
                </p>
              </div>
            </div>
          </div>

          {/* Botones de Acción */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link
              to="/categorias"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200"
            >
              Ver Categorías
            </Link>
            <Link
              to="/productos"
              className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200"
            >
              Ver Productos
            </Link>
          </div>

          {/* Footer Info */}
          <div className="text-sm text-gray-600 pt-8 border-t border-gray-300">
            <p>UTN - Unidad 7 • Desarrollo Full Stack • Python + React + TypeScript</p>
          </div>
        </div>
      </div>
    </div>
  );
}
