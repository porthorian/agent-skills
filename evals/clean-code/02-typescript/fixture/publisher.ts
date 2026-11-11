export type Writer = { write(topic: string): Promise<void> };

export async function publish(writer: Writer, topic: string): Promise<string> {
  const normalized = topic.trim();
  writer.write(normalized);
  return normalized;
}
