from project.godley_model import SFCModel, load_minsky_file, sanitize_xml, plot_history

model = SFCModel(dt=1.0)

# test_xml = """
# <root>
#   <variable name="TestStock" type="stock" init="100"/>
#   <godleyTable>
#     <row account="Assets">
#       <cell op="inflow">TestFlow</cell>
#     </row>
#   </godleyTable>
# </root>
# """

# with open("test.mky", "w") as f:
#     f.write(test_xml)

loaded_model = load_minsky_file(model, "test.mky")  # Should work

# clean_file = sanitize_xml("/workspaces/SFC_economic/minsky/Mice.mky")
# clean_file = sanitize_xml("/workspaces/SFC_economic/minsky/Financial Markets Pedator Prey.mky")

# loaded_model = load_minsky_file(model, clean_file)

# load_minsky_file(model, "project/minsky/Mice.mky")
# load_minsky_file(model, "/workspaces/SFC_economic/minsky/Mice.mky")
# loaded_model = load_minsky_file(model, "/workspaces/SFC_economic/minsky/Mice.clean.mky")
# load_minsky_file(model, "/workspaces/SFC_economic/minsky/Financial Markets Pedator Prey.mky")
# load_minsky_file(model, "/workspaces/SFC_economic/minsky/Automatic Stabilizers.mky")
# load_minsky_file(model, "./minsky/Mice.mky")


  #  loaded_model = load_minsky_file(model, "minsky/Mice.mky")
  #  assert loaded_model.stocks  # Should contain values

# print(load_minsky_file)

assert loaded_model.stocks  # Should contain values

history = loaded_model.run(T=20, return_history=True)

# Print result
for t, h in enumerate(history):
    print(f"t={t}: {h}")

# plot_history(file) # TODO
# df = pd.DataFrame(history)
# df.plot(title="Simulation Output from Minsky File")
# plt.xlabel("Time")
# plt.grid(True)
# plt.show()
