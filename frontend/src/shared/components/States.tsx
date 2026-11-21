interface StateProps {
  message: string;
}

export function LoadingState({ message }: StateProps) {
  return <p role="status" className="py-12 text-center text-gray-600">{message}</p>;
}

export function EmptyState({ message }: StateProps) {
  return <p className="py-12 text-center text-gray-500">{message}</p>;
}

export function ErrorState({ message }: StateProps) {
  return <p role="alert" className="my-4 rounded border border-red-400 bg-red-50 p-4 text-red-700">{message}</p>;
}
